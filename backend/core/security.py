"""Security module for JWT and password management"""
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password"""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Verify a hashed password"""
    return check_password_hash(hashed_password, password)

def create_tokens(identity):
    """Create access and refresh tokens for a user"""
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return {'access_token': access_token, 'refresh_token': refresh_token}
