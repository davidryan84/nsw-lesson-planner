"""Evidence Service - business logic for tracking student evidence"""
from backend.core.database import db
from backend.models.evidence import Evidence
from backend.models.student_progress import StudentProgress
from backend.models.learning_experience import LearningExperience
from datetime import datetime
import json

class EvidenceService:
    """Service for logging and managing evidence"""
    
    @staticmethod
    def log_evidence(teacher_id, student_id, learning_experience_id, observation_text, 
                    mastery_level, success_criteria_ids=None, lesson_id=None, 
                    attachment_url=None, notes=None):
        """
        Log evidence of student learning
        
        Args:
            teacher_id: ID of teacher logging evidence
            student_id: ID of student
            learning_experience_id: ID of LE being assessed
            observation_text: Description of observation
            mastery_level: 1-4 scale (Developing/Approaching/Meeting/Exceeding)
            success_criteria_ids: List of SC IDs demonstrated
            lesson_id: ID of lesson (optional)
            attachment_url: URL to photo/file (optional)
            notes: Additional notes (optional)
        
        Returns:
            Evidence object
        """
        evidence = Evidence(
            teacher_id=teacher_id,
            student_id=student_id,
            learning_experience_id=learning_experience_id,
            lesson_id=lesson_id,
            observation_date=datetime.utcnow(),
            observation_text=observation_text,
            mastery_level=mastery_level,
            attachment_url=attachment_url,
            notes=notes
        )
        
        if success_criteria_ids:
            evidence.set_success_criteria_ids(success_criteria_ids)
        
        db.session.add(evidence)
        db.session.commit()
        
        # Update student progress
        StudentProgressService.update_progress(student_id, learning_experience_id)
        
        return evidence
    
    @staticmethod
    def get_evidence(evidence_id):
        """Get evidence by ID"""
        return Evidence.query_by_id(evidence_id)
    
    @staticmethod
    def get_student_evidence(student_id):
        """Get all evidence for a student"""
        return Evidence.find_by_student(student_id)
    
    @staticmethod
    def get_student_le_evidence(student_id, learning_experience_id):
        """Get evidence for student on specific LE"""
        return Evidence.find_by_student_and_le(student_id, learning_experience_id)
    
    @staticmethod
    def get_teacher_evidence(teacher_id):
        """Get all evidence logged by teacher"""
        return Evidence.find_by_teacher(teacher_id)
    
    @staticmethod
    def update_evidence(evidence_id, **kwargs):
        """Update an evidence entry"""
        evidence = Evidence.query_by_id(evidence_id)
        if not evidence:
            return None
        
        for key, value in kwargs.items():
            if hasattr(evidence, key):
                setattr(evidence, key, value)
        
        db.session.commit()
        
        # Update progress after change
        StudentProgressService.update_progress(evidence.student_id, evidence.learning_experience_id)
        
        return evidence
    
    @staticmethod
    def delete_evidence(evidence_id):
        """Delete an evidence entry"""
        evidence = Evidence.query_by_id(evidence_id)
        if not evidence:
            return None
        
        student_id = evidence.student_id
        le_id = evidence.learning_experience_id
        
        db.session.delete(evidence)
        db.session.commit()
        
        # Recalculate progress after deletion
        StudentProgressService.update_progress(student_id, le_id)
        
        return True
