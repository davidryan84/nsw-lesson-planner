"""Input validation utilities"""
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    return len(password) >= 8

def validate_required_fields(data, required_fields):
    """Check that required fields are present"""
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True
