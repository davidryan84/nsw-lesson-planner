"""Lesson model - instance of a Learning Experience in a weekly plan"""
from backend.core.database import BaseModel, db
from datetime import datetime

class Lesson(BaseModel):
    """Lesson model - scheduled instance of a Learning Experience"""
    __tablename__ = 'lessons'
    
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False, index=True)
    learning_experience_id = db.Column(db.String(36), db.ForeignKey('learning_experiences.id'), nullable=False, index=True)
    week_number = db.Column(db.Integer, nullable=False)
    date_scheduled = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, published, taught, archived
    
    def __repr__(self):
        return f'<Lesson Week {self.week_number} - {self.date_scheduled.date()}>'
    
    @classmethod
    def find_by_teacher_and_week(cls, teacher_id, week_number):
        """Get all lessons for a teacher in a specific week"""
        return cls.query.filter_by(teacher_id=teacher_id, week_number=week_number, status='published').all()
    
    @classmethod
    def find_by_teacher(cls, teacher_id):
        """Get all lessons for a teacher"""
        return cls.query.filter_by(teacher_id=teacher_id).order_by(cls.date_scheduled).all()
    
    @classmethod
    def find_by_le(cls, learning_experience_id):
        """Get all scheduled lessons for a Learning Experience"""
        return cls.query.filter_by(learning_experience_id=learning_experience_id).all()
    
    def publish(self):
        """Publish lesson to make it visible in weekly plan"""
        self.status = 'published'
        db.session.commit()
        return self
    
    def mark_taught(self):
        """Mark lesson as taught"""
        self.status = 'taught'
        db.session.commit()
        return self
    
    def archive(self):
        """Archive lesson"""
        self.status = 'archived'
        db.session.commit()
        return self
