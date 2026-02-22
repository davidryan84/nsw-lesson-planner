"""Authentication endpoints"""
from flask import request, jsonify
from backend.core.security import hash_password, verify_password, create_tokens
from backend.models.teacher import Teacher
from backend.core.database import db
from . import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new teacher"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Email and password required'}, 400
    
    if Teacher.find_by_email(data['email']):
        return {'error': 'Email already registered'}, 400
    
    teacher = Teacher(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        password_hash=hash_password(data['password'])
    )
    
    db.session.add(teacher)
    db.session.commit()
    
    tokens = create_tokens(teacher.id)
    return {**tokens, 'teacher': teacher.to_dict()}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a teacher"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Email and password required'}, 400
    
    teacher = Teacher.find_by_email(data['email'])
    
    if not teacher or not verify_password(teacher.password_hash, data['password']):
        return {'error': 'Invalid email or password'}, 401
    
    tokens = create_tokens(teacher.id)
    return {**tokens, 'teacher': teacher.to_dict()}, 200
