"""Evidence model - tracking student learning"""
from backend.core.database import BaseModel, db
import json

class Evidence(BaseModel):
    """Evidence of student learning against success criteria"""
    __tablename__ = 'evidence'
    
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False, index=True)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False, index=True)
    learning_experience_id = db.Column(db.String(36), db.ForeignKey('learning_experiences.id'), nullable=False, index=True)
    lesson_id = db.Column(db.String(36), db.ForeignKey('lessons.id'))
    
    observation_date = db.Column(db.DateTime, nullable=False)
    observation_text = db.Column(db.Text, nullable=False)
    
    # Mastery level: 1=Developing, 2=Approaching, 3=Meeting, 4=Exceeding
    mastery_level = db.Column(db.Integer, nullable=False)
    
    # Success criteria demonstrated (JSON array of SC IDs)
    success_criteria_ids = db.Column(db.Text)
    
    # File attachment (photo, work sample, etc.)
    attachment_url = db.Column(db.String(500))
    
    # Notes from teacher
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Evidence Student {self.student_id} - LE {self.learning_experience_id}>'
    
    def get_success_criteria_ids(self):
        """Get success criteria IDs as list"""
        try:
            return json.loads(self.success_criteria_ids) if self.success_criteria_ids else []
        except:
            return []
    
    def set_success_criteria_ids(self, ids_list):
        """Set success criteria IDs from list"""
        self.success_criteria_ids = json.dumps(ids_list)
    
    @classmethod
    def find_by_student(cls, student_id):
        """Get all evidence for a student"""
        return cls.query.filter_by(student_id=student_id).order_by(cls.observation_date.desc()).all()
    
    @classmethod
    def find_by_student_and_le(cls, student_id, learning_experience_id):
        """Get all evidence for a student for a specific LE"""
        return cls.query.filter_by(student_id=student_id, learning_experience_id=learning_experience_id).all()
    
    @classmethod
    def find_by_teacher(cls, teacher_id):
        """Get all evidence logged by a teacher"""
        return cls.query.filter_by(teacher_id=teacher_id).order_by(cls.observation_date.desc()).all()
