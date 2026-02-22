"""Worksheet endpoints"""
from flask import request, jsonify
from backend.models.worksheet import Worksheet
from backend.core.database import db
from . import worksheets_bp

@worksheets_bp.route('', methods=['GET'])
def get_worksheets():
    """Get all worksheets"""
    worksheets = Worksheet.query.all()
    return {'worksheets': [w.to_dict() for w in worksheets]}, 200

@worksheets_bp.route('/<worksheet_id>', methods=['GET'])
def get_worksheet(worksheet_id):
    """Get a specific worksheet"""
    worksheet = Worksheet.query_by_id(worksheet_id)
    if not worksheet:
        return {'error': 'Worksheet not found'}, 404
    return {'worksheet': worksheet.to_dict()}, 200

@worksheets_bp.route('', methods=['POST'])
def create_worksheet():
    """Create a new worksheet"""
    data = request.get_json()
    
    worksheet = Worksheet(
        title=data.get('title'),
        description=data.get('description'),
        subject=data.get('subject'),
        year_level=data.get('year_level')
    )
    
    db.session.add(worksheet)
    db.session.commit()
    
    return {'worksheet': worksheet.to_dict()}, 201
