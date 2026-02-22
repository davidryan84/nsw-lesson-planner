"""Health check endpoint"""
from . import health_bp

@health_bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'NSW Lesson Planner'}, 200
