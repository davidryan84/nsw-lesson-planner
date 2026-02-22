"""Student endpoints"""
from flask import request
from backend.models.student import Student
from backend.core.database import db
from . import students_bp

@students_bp.route('', methods=['GET'])
def get_students():
    """Get all students"""
    students = Student.query.all()
    return {'students': [s.to_dict() for s in students]}, 200

@students_bp.route('', methods=['POST'])
def create_student():
    """Create a new student"""
    data = request.get_json()
    
    student = Student(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        year_level=data.get('year_level')
    )
    
    db.session.add(student)
    db.session.commit()
    
    return {'student': student.to_dict()}, 201
