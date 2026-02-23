"""Learning Experience Service"""
from backend.core.database import db
from backend.models.learning_experience import LearningExperience
import json

class LearningExperienceService:
    """Service for managing Learning Experiences"""
    
    @staticmethod
    def create_le(teacher_id, unit_number, experience_number, core_concept, 
                  learning_intention, success_criteria, subject, year_level=6, 
                  nesa_outcome_code=None, duration_minutes=60):
        """Create a new Learning Experience"""
        
        # Convert success criteria to JSON if it's a list
        if isinstance(success_criteria, list):
            success_criteria = json.dumps(success_criteria)
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=unit_number,
            experience_number=experience_number,
            core_concept=core_concept,
            learning_intention=learning_intention,
            success_criteria=success_criteria,
            subject=subject,
            year_level=year_level,
            nesa_outcome_code=nesa_outcome_code,
            duration_minutes=duration_minutes
        )
        
        db.session.add(le)
        db.session.commit()
        return le
    
    @staticmethod
    def get_le(le_id):
        """Get a Learning Experience by ID"""
        return LearningExperience.query_by_id(le_id)
    
    @staticmethod
    def get_all_les(teacher_id):
        """Get all Learning Experiences for a teacher"""
        return LearningExperience.find_by_teacher(teacher_id)
    
    @staticmethod
    def get_les_by_unit(teacher_id, unit_number):
        """Get Learning Experiences for a specific unit"""
        return LearningExperience.find_by_unit(teacher_id, unit_number)
    
    @staticmethod
    def update_le(le_id, **kwargs):
        """Update a Learning Experience"""
        le = LearningExperience.query_by_id(le_id)
        if not le:
            return None
        
        # Handle success criteria conversion
        if 'success_criteria' in kwargs and isinstance(kwargs['success_criteria'], list):
            kwargs['success_criteria'] = json.dumps(kwargs['success_criteria'])
        
        for key, value in kwargs.items():
            if hasattr(le, key):
                setattr(le, key, value)
        
        db.session.commit()
        return le
    
    @staticmethod
    def delete_le(le_id):
        """Soft delete a Learning Experience (mark inactive)"""
        le = LearningExperience.query_by_id(le_id)
        if not le:
            return False
        
        le.is_active = False
        db.session.commit()
        return True
    
    @staticmethod
    def get_success_criteria(le_id):
        """Get success criteria for a Learning Experience"""
        le = LearningExperience.query_by_id(le_id)
        if not le:
            return None
        
        return le.get_success_criteria_list()
