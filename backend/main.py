"""
Flask Application Factory
Creates and configures the Flask app with all blueprints and extensions
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import RotatingFileHandler
import os

# Import database AFTER defining it
from backend.core.database import db

# Initialize JWT
jwt = JWTManager()

def create_app(config_name='development'):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment (development, production, testing)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from backend.config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from backend.config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from backend.config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints and create tables
    with app.app_context():
        # Import models AFTER db is initialized
        from backend.models.teacher import Teacher
        from backend.models.student import Student
        from backend.models.worksheet import Worksheet
        from backend.models.worksheet_question import WorksheetQuestion
        from backend.models.learning_experience import LearningExperience
        from backend.models.lesson import Lesson
        from backend.models.evidence import Evidence
        from backend.models.student_progress import StudentProgress
        
        from backend.api.v1 import (auth_bp, worksheets_bp, students_bp, 
                                    evidence_bp, health_bp, le_bp, lessons_bp)
        from backend.api.v1.worksheets_routes import worksheets_routes_bp
        from backend.api.v1.evidence_routes import evidence_routes_bp
        from backend.api.v1.support_files_routes import support_files_bp
        
        app.register_blueprint(health_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(worksheets_bp)
        app.register_blueprint(students_bp)
        app.register_blueprint(evidence_bp)
        app.register_blueprint(le_bp)
        app.register_blueprint(lessons_bp)
        app.register_blueprint(worksheets_routes_bp)
        app.register_blueprint(evidence_routes_bp)
        app.register_blueprint(support_files_bp)
        
        # Create database tables
        db.create_all()
    
    # Configure logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('NSW Lesson Planner startup')
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
