"""Worksheet model"""
from backend.core.database import BaseModel, db

class Worksheet(BaseModel):
    """Worksheet model - collection of questions at one tier level"""
    __tablename__ = 'worksheets'
    
    lesson_id = db.Column(db.String(36), db.ForeignKey('lessons.id'), nullable=False, index=True)
    tier = db.Column(db.String(20), nullable=False)  # mild, medium, spicy, enrichment
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50), nullable=False)
    year_level = db.Column(db.Integer, nullable=False)
    learning_intention = db.Column(db.Text)
    success_criteria = db.Column(db.Text)  # JSON
    question_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(500))  # Path to generated .docx file
    
    def __repr__(self):
        return f'<Worksheet {self.tier} - {self.question_count} questions>'
    
    @classmethod
    def find_by_lesson(cls, lesson_id):
        """Get all worksheets for a lesson"""
        return cls.query.filter_by(lesson_id=lesson_id).all()
    
    @classmethod
    def find_by_lesson_and_tier(cls, lesson_id, tier):
        """Get worksheet for a specific tier"""
        return cls.query.filter_by(lesson_id=lesson_id, tier=tier).first()
