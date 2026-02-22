"""Decorators for Flask routes"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from .errors import AuthenticationError

def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            raise AuthenticationError('Missing or invalid token')
        return f(*args, **kwargs)
    return decorated_function
