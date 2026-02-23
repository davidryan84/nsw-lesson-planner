"""Student Progress Service - aggregates evidence into progress"""
from backend.core.database import db
from backend.models.student_progress import StudentProgress
from backend.models.evidence import Evidence
from backend.models.learning_experience import LearningExperience
from datetime import datetime
import json

class StudentProgressService:
    """Service for tracking and aggregating student progress"""
    
    @staticmethod
    def update_progress(student_id, learning_experience_id):
        """
        Update student progress by aggregating all evidence
        
        Args:
            student_id: ID of student
            learning_experience_id: ID of LE
        
        Returns:
            Updated StudentProgress object
        """
        # Get or create progress record
        progress = StudentProgress.find_by_student_and_le(student_id, learning_experience_id)
        if not progress:
            progress = StudentProgress(
                student_id=student_id,
                learning_experience_id=learning_experience_id
            )
            db.session.add(progress)
        
        # Get all evidence
        evidence_list = Evidence.find_by_student_and_le(student_id, learning_experience_id)
        
        if not evidence_list:
            db.session.commit()
            return progress
        
        # Calculate mastery level (take highest)
        mastery_levels = [e.mastery_level for e in evidence_list]
        progress.mastery_level = max(mastery_levels)
        progress.evidence_count = len(evidence_list)
        progress.last_evidence_date = evidence_list[0].observation_date
        
        # Get LE to find success criteria
        le = LearningExperience.query_by_id(learning_experience_id)
        if le:
            sc_list = le.get_success_criteria_list()
            sc_status = {}
            
            # Check if each SC was demonstrated
            for i, sc in enumerate(sc_list):
                sc_id = str(i)  # Use index as ID
                demonstrated = any(
                    sc_id in e.get_success_criteria_ids() for e in evidence_list
                )
                sc_status[sc_id] = 'met' if demonstrated else 'not_met'
            
            progress.set_success_criteria_status(sc_status)
        
        # Calculate trend (comparing recent vs older evidence)
        if len(evidence_list) >= 2:
            recent_levels = [e.mastery_level for e in evidence_list[:3]]
            older_levels = [e.mastery_level for e in evidence_list[3:]]
            
            if older_levels:
                recent_avg = sum(recent_levels) / len(recent_levels)
                older_avg = sum(older_levels) / len(older_levels)
                
                if recent_avg > older_avg:
                    progress.trend = 'improving'
                elif recent_avg < older_avg:
                    progress.trend = 'declining'
                else:
                    progress.trend = 'stable'
        
        db.session.commit()
        return progress
    
    @staticmethod
    def get_progress(student_id, learning_experience_id):
        """Get progress for student on LE"""
        return StudentProgress.find_by_student_and_le(student_id, learning_experience_id)
    
    @staticmethod
    def get_student_progress(student_id):
        """Get all progress for a student"""
        return StudentProgress.find_by_student(student_id)
    
    @staticmethod
    def get_class_progress(learning_experience_id):
        """Get progress for all students on a LE"""
        return StudentProgress.query.filter_by(learning_experience_id=learning_experience_id).all()
