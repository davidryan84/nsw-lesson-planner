"""Lessons API endpoints"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.lesson_service import LessonService
from flask import Blueprint
from datetime import datetime

lessons_bp = Blueprint('lessons', __name__, url_prefix='/api/v1/lessons')

@lessons_bp.route('', methods=['POST'])
@jwt_required()
def create_lesson():
    """Create a new Lesson"""
    teacher_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['learning_experience_id', 'week_number', 'date_scheduled']
    
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}, 400
    
    try:
        # Parse date_scheduled
        date_scheduled = datetime.fromisoformat(data['date_scheduled'])
        
        lesson = LessonService.create_lesson(
            teacher_id=teacher_id,
            learning_experience_id=data['learning_experience_id'],
            week_number=data['week_number'],
            date_scheduled=date_scheduled,
            duration_minutes=data.get('duration_minutes', 60),
            location=data.get('location'),
            notes=data.get('notes')
        )
        
        if not lesson:
            return {'error': 'Learning Experience not found or unauthorized'}, 404
        
        return {'lesson': lesson.to_dict()}, 201
    
    except ValueError:
        return {'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}, 400
    except Exception as e:
        return {'error': str(e)}, 500

@lessons_bp.route('', methods=['GET'])
@jwt_required()
def get_lessons():
    """Get lessons for logged-in teacher"""
    teacher_id = get_jwt_identity()
    week_number = request.args.get('week_number', type=int)
    
    if week_number:
        lessons = LessonService.get_week_lessons(teacher_id, week_number)
    else:
        lessons = LessonService.get_all_lessons(teacher_id)
    
    return {'lessons': [l.to_dict() for l in lessons]}, 200

@lessons_bp.route('/<lesson_id>', methods=['GET'])
@jwt_required()
def get_lesson(lesson_id):
    """Get a specific lesson"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    return {'lesson': lesson.to_dict()}, 200

@lessons_bp.route('/<lesson_id>', methods=['PUT'])
@jwt_required()
def update_lesson(lesson_id):
    """Update a lesson"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    try:
        # Parse date_scheduled if provided
        if 'date_scheduled' in data:
            data['date_scheduled'] = datetime.fromisoformat(data['date_scheduled'])
        
        updated_lesson = LessonService.update_lesson(lesson_id, **data)
        return {'lesson': updated_lesson.to_dict()}, 200
    
    except ValueError:
        return {'error': 'Invalid date format'}, 400
    except Exception as e:
        return {'error': str(e)}, 500

@lessons_bp.route('/<lesson_id>/publish', methods=['POST'])
@jwt_required()
def publish_lesson(lesson_id):
    """Publish a lesson"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    lesson = LessonService.publish_lesson(lesson_id)
    return {'lesson': lesson.to_dict()}, 200

@lessons_bp.route('/<lesson_id>/mark-taught', methods=['POST'])
@jwt_required()
def mark_lesson_taught(lesson_id):
    """Mark a lesson as taught"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    lesson = LessonService.mark_lesson_taught(lesson_id)
    return {'lesson': lesson.to_dict()}, 200

@lessons_bp.route('/<lesson_id>/archive', methods=['POST'])
@jwt_required()
def archive_lesson(lesson_id):
    """Archive a lesson"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    lesson = LessonService.archive_lesson(lesson_id)
    return {'lesson': lesson.to_dict()}, 200

@lessons_bp.route('/<lesson_id>', methods=['DELETE'])
@jwt_required()
def delete_lesson(lesson_id):
    """Delete a lesson"""
    teacher_id = get_jwt_identity()
    lesson = LessonService.get_lesson(lesson_id)
    
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    LessonService.delete_lesson(lesson_id)
    return {'message': 'Lesson deleted'}, 200
