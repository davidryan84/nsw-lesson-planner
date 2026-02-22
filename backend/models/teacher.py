"""Teacher model"""
from backend.core.database import BaseModel, db

class Teacher(BaseModel):
    """Teacher model"""
    __tablename__ = 'teachers'
    
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Teacher {self.email}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
