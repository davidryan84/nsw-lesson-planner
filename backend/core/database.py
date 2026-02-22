"""
Database Configuration and Models
SQLAlchemy setup with BaseModel for all database operations
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base model with common fields for all models"""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def to_json(self):
        """Convert model to JSON-serializable dict"""
        return self.to_dict()
    
    def save(self):
        """Save model to database"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete model from database"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def query_by_id(cls, id):
        """Query model by ID"""
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def query_all(cls):
        """Query all instances of model"""
        return cls.query.all()
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
