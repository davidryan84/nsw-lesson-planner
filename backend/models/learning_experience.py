"""Learning Experience model"""
from backend.core.database import BaseModel, db
import json

class LearningExperience(BaseModel):
    """Learning Experience model - core lesson concept"""
    __tablename__ = 'learning_experiences'
    
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False, index=True)
    unit_number = db.Column(db.Integer, nullable=False)
    experience_number = db.Column(db.Integer, nullable=False)
    core_concept = db.Column(db.String(200), nullable=False)
    learning_intention = db.Column(db.Text, nullable=False)
    success_criteria = db.Column(db.Text, nullable=False)  # JSON array of "I can..." statements
    subject = db.Column(db.String(50), nullable=False)  # Maths, English, Science, History, Geography
    year_level = db.Column(db.Integer, nullable=False, default=6)
    nesa_outcome_code = db.Column(db.String(50))  # e.g., "MA3-RN-01"
    duration_minutes = db.Column(db.Integer, default=60)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<LearningExperience Unit {self.unit_number} LE {self.experience_number}>'
    
    def get_success_criteria_list(self):
        """Get success criteria as list"""
        try:
            return json.loads(self.success_criteria)
        except:
            return [self.success_criteria]
    
    def set_success_criteria_list(self, criteria_list):
        """Set success criteria from list"""
        self.success_criteria = json.dumps(criteria_list)
    
    @classmethod
    def find_by_teacher(cls, teacher_id):
        """Get all LEs for a teacher"""
        return cls.query.filter_by(teacher_id=teacher_id, is_active=True).all()
    
    @classmethod
    def find_by_unit(cls, teacher_id, unit_number):
        """Get LEs for specific unit"""
        return cls.query.filter_by(teacher_id=teacher_id, unit_number=unit_number, is_active=True).all()
