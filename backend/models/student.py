"""Student model"""
from backend.core.database import BaseModel, db

class Student(BaseModel):
    """Student model"""
    __tablename__ = 'students'
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
