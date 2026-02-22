"""Evidence endpoints"""
from flask import request
from . import evidence_bp

@evidence_bp.route('', methods=['POST'])
def log_evidence():
    """Log student evidence/observation"""
    data = request.get_json()
    
    # Simple placeholder - extend with real model
    return {'message': 'Evidence logged successfully'}, 201

@evidence_bp.route('', methods=['GET'])
def get_evidence():
    """Get all evidence"""
    return {'evidence': []}, 200
