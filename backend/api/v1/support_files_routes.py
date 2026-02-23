"""Support Files API endpoints - generate teacher resources"""
from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.support_files_service import SupportFilesService
from backend.services.lesson_service import LessonService
from flask import Blueprint
import os

support_files_bp = Blueprint('support_files', __name__, url_prefix='/api/v1/support-files')

@support_files_bp.route('/generate/<lesson_id>', methods=['POST'])
@jwt_required()
def generate_support_files(lesson_id):
    """Generate all support files for a lesson"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    try:
        # Generate files
        results = SupportFilesService.generate_all(lesson_id, output_dir='/tmp')
        
        return {
            'message': 'Support files generated successfully',
            'files': results
        }, 201
    
    except Exception as e:
        return {'error': str(e)}, 500

@support_files_bp.route('/teacher-guide/<lesson_id>', methods=['POST'])
@jwt_required()
def generate_teacher_guide(lesson_id):
    """Generate only teacher guide"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    try:
        result = SupportFilesService.generate_teacher_guide(lesson_id, output_dir='/tmp')
        if result:
            return {'file': result}, 201
        return {'error': 'Failed to generate teacher guide'}, 500
    except Exception as e:
        return {'error': str(e)}, 500

@support_files_bp.route('/answer-sheet/<lesson_id>', methods=['POST'])
@jwt_required()
def generate_answer_sheet(lesson_id):
    """Generate only answer sheet"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    try:
        result = SupportFilesService.generate_answer_sheet(lesson_id, output_dir='/tmp')
        if result:
            return {'file': result}, 201
        return {'error': 'Failed to generate answer sheet'}, 500
    except Exception as e:
        return {'error': str(e)}, 500

@support_files_bp.route('/exemplar/<lesson_id>', methods=['POST'])
@jwt_required()
def generate_exemplar(lesson_id):
    """Generate only exemplar"""
    teacher_id = get_jwt_identity()
    
    lesson = LessonService.get_lesson(lesson_id)
    if not lesson:
        return {'error': 'Lesson not found'}, 404
    
    if lesson.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    try:
        result = SupportFilesService.generate_exemplar(lesson_id, output_dir='/tmp')
        if result:
            return {'file': result}, 201
        return {'error': 'Failed to generate exemplar'}, 500
    except Exception as e:
        return {'error': str(e)}, 500
