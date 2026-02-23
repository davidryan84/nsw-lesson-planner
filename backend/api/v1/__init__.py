"""API v1 blueprints"""
from flask import Blueprint

# Create blueprints
health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
worksheets_bp = Blueprint('worksheets', __name__, url_prefix='/api/v1/worksheets')
students_bp = Blueprint('students', __name__, url_prefix='/api/v1/students')
evidence_bp = Blueprint('evidence', __name__, url_prefix='/api/v1/evidence')

# Import new blueprints
from backend.api.v1.learning_experiences import le_bp
from backend.api.v1.lessons import lessons_bp

# Import routes
from . import health, auth, worksheets, students, evidence
