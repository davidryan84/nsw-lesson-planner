"""Evidence tracking API endpoints"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.evidence_service import EvidenceService
from backend.services.student_progress_service import StudentProgressService
from backend.services.lesson_service import LessonService
from datetime import datetime
from flask import Blueprint

evidence_routes_bp = Blueprint('evidence_routes', __name__, url_prefix='/api/v1/evidence')

@evidence_routes_bp.route('', methods=['POST'])
@jwt_required()
def log_evidence():
    """Log evidence of student learning"""
    teacher_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['student_id', 'learning_experience_id', 'observation_text', 'mastery_level']
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}, 400
    
    # Validate mastery level
    mastery_level = data['mastery_level']
    if mastery_level not in [1, 2, 3, 4]:
        return {'error': 'Mastery level must be 1-4'}, 400
    
    try:
        evidence = EvidenceService.log_evidence(
            teacher_id=teacher_id,
            student_id=data['student_id'],
            learning_experience_id=data['learning_experience_id'],
            observation_text=data['observation_text'],
            mastery_level=mastery_level,
            success_criteria_ids=data.get('success_criteria_ids'),
            lesson_id=data.get('lesson_id'),
            attachment_url=data.get('attachment_url'),
            notes=data.get('notes')
        )
        
        return {'evidence': evidence.to_dict()}, 201
    
    except Exception as e:
        return {'error': str(e)}, 500

@evidence_routes_bp.route('/student/<student_id>', methods=['GET'])
@jwt_required()
def get_student_evidence(student_id):
    """Get all evidence for a student"""
    teacher_id = get_jwt_identity()
    
    # Get evidence
    evidence_list = EvidenceService.get_student_evidence(student_id)
    
    return {
        'evidence': [e.to_dict() for e in evidence_list]
    }, 200

@evidence_routes_bp.route('/student/<student_id>/le/<le_id>', methods=['GET'])
@jwt_required()
def get_student_le_evidence(student_id, le_id):
    """Get evidence for student on specific LE"""
    teacher_id = get_jwt_identity()
    
    evidence_list = EvidenceService.get_student_le_evidence(student_id, le_id)
    progress = StudentProgressService.get_progress(student_id, le_id)
    
    return {
        'evidence': [e.to_dict() for e in evidence_list],
        'progress': progress.to_dict() if progress else None
    }, 200

@evidence_routes_bp.route('/<evidence_id>', methods=['GET'])
@jwt_required()
def get_evidence(evidence_id):
    """Get specific evidence entry"""
    teacher_id = get_jwt_identity()
    
    evidence = EvidenceService.get_evidence(evidence_id)
    if not evidence:
        return {'error': 'Evidence not found'}, 404
    
    if evidence.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    return {'evidence': evidence.to_dict()}, 200

@evidence_routes_bp.route('/<evidence_id>', methods=['PUT'])
@jwt_required()
def update_evidence(evidence_id):
    """Update an evidence entry"""
    teacher_id = get_jwt_identity()
    
    evidence = EvidenceService.get_evidence(evidence_id)
    if not evidence:
        return {'error': 'Evidence not found'}, 404
    
    if evidence.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    try:
        updated = EvidenceService.update_evidence(evidence_id, **data)
        return {'evidence': updated.to_dict()}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@evidence_routes_bp.route('/<evidence_id>', methods=['DELETE'])
@jwt_required()
def delete_evidence(evidence_id):
    """Delete an evidence entry"""
    teacher_id = get_jwt_identity()
    
    evidence = EvidenceService.get_evidence(evidence_id)
    if not evidence:
        return {'error': 'Evidence not found'}, 404
    
    if evidence.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    EvidenceService.delete_evidence(evidence_id)
    return {'message': 'Evidence deleted'}, 200

@evidence_routes_bp.route('/progress/student/<student_id>', methods=['GET'])
@jwt_required()
def get_student_progress(student_id):
    """Get all progress for a student"""
    teacher_id = get_jwt_identity()
    
    progress_list = StudentProgressService.get_student_progress(student_id)
    
    return {
        'progress': [p.to_dict() for p in progress_list]
    }, 200

@evidence_routes_bp.route('/progress/le/<le_id>', methods=['GET'])
@jwt_required()
def get_le_progress(le_id):
    """Get class progress on a LE"""
    teacher_id = get_jwt_identity()
    
    progress_list = StudentProgressService.get_class_progress(le_id)
    
    # Filter to only show progress for students in teacher's classes
    # (In real app, would verify teacher has access to these students)
    
    return {
        'progress': [p.to_dict() for p in progress_list]
    }, 200
