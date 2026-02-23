"""Student Progress model - aggregated learning progress"""
from backend.core.database import BaseModel, db
import json

class StudentProgress(BaseModel):
    """Aggregated progress for a student on a Learning Experience"""
    __tablename__ = 'student_progress'
    
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False, index=True)
    learning_experience_id = db.Column(db.String(36), db.ForeignKey('learning_experiences.id'), nullable=False, index=True)
    
    # Current mastery level (1-4)
    mastery_level = db.Column(db.Integer, default=1)
    
    # Success criteria status (JSON: {sc_id: 'met'|'not_met'|'emerging'})
    success_criteria_status = db.Column(db.Text)
    
    # Number of evidence entries
    evidence_count = db.Column(db.Integer, default=0)
    
    # Progress trend: 'improving', 'stable', 'declining'
    trend = db.Column(db.String(50), default='stable')
    
    # Last evidence date
    last_evidence_date = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<StudentProgress {self.student_id} - LE {self.learning_experience_id}>'
    
    def get_success_criteria_status(self):
        """Get SC status as dict"""
        try:
            return json.loads(self.success_criteria_status) if self.success_criteria_status else {}
        except:
            return {}
    
    def set_success_criteria_status(self, status_dict):
        """Set SC status from dict"""
        self.success_criteria_status = json.dumps(status_dict)
    
    @classmethod
    def find_by_student(cls, student_id):
        """Get all progress for a student"""
        return cls.query.filter_by(student_id=student_id).all()
    
    @classmethod
    def find_by_student_and_le(cls, student_id, learning_experience_id):
        """Get progress for student on specific LE"""
        return cls.query.filter_by(student_id=student_id, learning_experience_id=learning_experience_id).first()
