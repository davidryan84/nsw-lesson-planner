"""Learning Experiences API endpoints"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.learning_experience_service import LearningExperienceService
from backend.core.errors import ValidationError, NotFoundError
from . import worksheets_bp

# Use worksheets_bp and add a new blueprint
from flask import Blueprint
le_bp = Blueprint('learning_experiences', __name__, url_prefix='/api/v1/learning-experiences')

@le_bp.route('', methods=['POST'])
@jwt_required()
def create_learning_experience():
    """Create a new Learning Experience"""
    teacher_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['unit_number', 'experience_number', 'core_concept', 
                      'learning_intention', 'success_criteria', 'subject']
    
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}, 400
    
    try:
        le = LearningExperienceService.create_le(
            teacher_id=teacher_id,
            unit_number=data['unit_number'],
            experience_number=data['experience_number'],
            core_concept=data['core_concept'],
            learning_intention=data['learning_intention'],
            success_criteria=data['success_criteria'],
            subject=data['subject'],
            year_level=data.get('year_level', 6),
            nesa_outcome_code=data.get('nesa_outcome_code')
        )
        
        return {'learning_experience': le.to_dict()}, 201
    
    except Exception as e:
        return {'error': str(e)}, 500

@le_bp.route('', methods=['GET'])
@jwt_required()
def get_learning_experiences():
    """Get all Learning Experiences for logged-in teacher"""
    teacher_id = get_jwt_identity()
    
    unit_number = request.args.get('unit_number', type=int)
    
    if unit_number:
        les = LearningExperienceService.get_les_by_unit(teacher_id, unit_number)
    else:
        les = LearningExperienceService.get_all_les(teacher_id)
    
    return {'learning_experiences': [le.to_dict() for le in les]}, 200

@le_bp.route('/<le_id>', methods=['GET'])
@jwt_required()
def get_learning_experience(le_id):
    """Get a specific Learning Experience"""
    teacher_id = get_jwt_identity()
    le = LearningExperienceService.get_le(le_id)
    
    if not le:
        return {'error': 'Learning Experience not found'}, 404
    
    if le.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    return {'learning_experience': le.to_dict()}, 200

@le_bp.route('/<le_id>', methods=['PUT'])
@jwt_required()
def update_learning_experience(le_id):
    """Update a Learning Experience"""
    teacher_id = get_jwt_identity()
    le = LearningExperienceService.get_le(le_id)
    
    if not le:
        return {'error': 'Learning Experience not found'}, 404
    
    if le.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    try:
        updated_le = LearningExperienceService.update_le(le_id, **data)
        return {'learning_experience': updated_le.to_dict()}, 200
    
    except Exception as e:
        return {'error': str(e)}, 500

@le_bp.route('/<le_id>', methods=['DELETE'])
@jwt_required()
def delete_learning_experience(le_id):
    """Delete (archive) a Learning Experience"""
    teacher_id = get_jwt_identity()
    le = LearningExperienceService.get_le(le_id)
    
    if not le:
        return {'error': 'Learning Experience not found'}, 404
    
    if le.teacher_id != teacher_id:
        return {'error': 'Unauthorized'}, 403
    
    LearningExperienceService.delete_le(le_id)
    return {'message': 'Learning Experience archived'}, 200
