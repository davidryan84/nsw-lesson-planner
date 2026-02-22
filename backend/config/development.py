"""Development configuration"""
import os

class DevelopmentConfig:
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://nsw_user:nsw_password@localhost:5432/nsw_lesson_planner'
    )
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
