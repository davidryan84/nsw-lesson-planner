"""Worksheet model"""
from backend.core.database import BaseModel, db

class Worksheet(BaseModel):
    """Worksheet model"""
    __tablename__ = 'worksheets'
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50), nullable=False)
    year_level = db.Column(db.Integer, nullable=False)
    learning_intention = db.Column(db.Text)
    success_criteria = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Worksheet {self.title}>'
