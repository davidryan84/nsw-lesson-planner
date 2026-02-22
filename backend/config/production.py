"""Production configuration"""
import os

class ProductionConfig:
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
