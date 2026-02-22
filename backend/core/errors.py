"""Custom exception classes"""

class APIError(Exception):
    """Base API error"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
    
    def to_dict(self):
        return {'error': self.message}

class ValidationError(APIError):
    """Validation error (400)"""
    def __init__(self, message):
        super().__init__(message, 400)

class AuthenticationError(APIError):
    """Authentication error (401)"""
    def __init__(self, message='Unauthorized'):
        super().__init__(message, 401)

class NotFoundError(APIError):
    """Not found error (404)"""
    def __init__(self, message='Resource not found'):
        super().__init__(message, 404)
