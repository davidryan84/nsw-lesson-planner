"""Worksheets API endpoints"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.worksheet_service import WorksheetService
from backend.services.lesson_service import LessonService
from flask import Blueprint

worksheets_routes_bp = Blueprint('worksheets_routes', __name__, url_prefix='/api/v1/worksheets')

@worksheets_routes_bp.route('/generate/<lesson_id>', methods=['POST'])
@jwt_required()
def generate_worksheets(lesson_id):
    """Generate all four tiered worksheets for a lesson"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    try:
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        
        if not worksheets:
            return {'error': 'Failed to generate worksheets'}, 500
        
        return {
            'worksheets': {
                tier: ws.to_dict() for tier, ws in worksheets.items()
            }
        }, 201
    
    except Exception as e:
        return {'error': str(e)}, 500

@worksheets_routes_bp.route('/lesson/<lesson_id>', methods=['GET'])
@jwt_required()
def get_lesson_worksheets(lesson_id):
    """Get all worksheets for a lesson"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    worksheets = WorksheetService.get_worksheets_by_lesson(lesson_id)
    
    return {
        'worksheets': [ws.to_dict() for ws in worksheets]
    }, 200

@worksheets_routes_bp.route('/<worksheet_id>', methods=['GET'])
@jwt_required()
def get_worksheet(worksheet_id):
    """Get a specific worksheet with all questions"""
    teacher_id = get_jwt_identity()
    
    worksheet = WorksheetService.get_worksheet(worksheet_id)
    if not worksheet:
        return {'error': 'Worksheet not found'}, 404
    
    # Verify teacher owns this worksheet's lesson
    lesson = LessonService.get_lesson(worksheet.lesson_id)
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    # Get questions
    questions = WorksheetService.get_questions(worksheet_id)
    
    return {
        'worksheet': worksheet.to_dict(),
        'questions': [q.to_dict() for q in questions]
    }, 200

@worksheets_routes_bp.route('/<worksheet_id>/questions/<question_id>', methods=['PUT'])
@jwt_required()
def update_question(worksheet_id, question_id):
    """Update a question in a worksheet"""
    teacher_id = get_jwt_identity()
    
    worksheet = WorksheetService.get_worksheet(worksheet_id)
    if not worksheet:
        return {'error': 'Worksheet not found'}, 404
    
    # Verify teacher owns this worksheet's lesson
    lesson = LessonService.get_lesson(worksheet.lesson_id)
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    try:
        question = WorksheetService.update_question(question_id, **data)
        if not question:
            return {'error': 'Question not found'}, 404
        
        return {'question': question.to_dict()}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@worksheets_routes_bp.route('/<worksheet_id>/tier/<tier>', methods=['GET'])
@jwt_required()
def get_tier_worksheet(worksheet_id, tier):
    """Get worksheet for a specific tier"""
    teacher_id = get_jwt_identity()
    
    worksheet = WorksheetService.get_worksheet(worksheet_id)
    if not worksheet:
        return {'error': 'Worksheet not found'}, 404
    
    # Verify teacher owns this worksheet's lesson
    lesson = LessonService.get_lesson(worksheet.lesson_id)
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    if worksheet.tier != tier:
        return {'error': 'Tier mismatch'}, 400
    
    questions = WorksheetService.get_questions(worksheet_id)
    
    return {
        'worksheet': worksheet.to_dict(),
        'questions': [q.to_dict() for q in questions]
    }, 200
