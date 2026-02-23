"""Worksheet Question model"""
from backend.core.database import BaseModel, db

class WorksheetQuestion(BaseModel):
    """Individual question in a worksheet"""
    __tablename__ = 'worksheet_questions'
    
    worksheet_id = db.Column(db.String(36), db.ForeignKey('worksheets.id'), nullable=False, index=True)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    tier = db.Column(db.String(20), nullable=False)  # mild, medium, spicy, enrichment
    hints = db.Column(db.Text)  # For Mild tier - JSON array
    model_answer = db.Column(db.Text)
    difficulty_level = db.Column(db.String(50))  # Based on Bloom's taxonomy
    
    def __repr__(self):
        return f'<WorksheetQuestion {self.question_number} - {self.tier}>'
    
    @classmethod
    def find_by_worksheet(cls, worksheet_id):
        """Get all questions for a worksheet"""
        return cls.query.filter_by(worksheet_id=worksheet_id).order_by(cls.question_number).all()
