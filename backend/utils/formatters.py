"""Data formatting utilities"""
from datetime import datetime

def format_datetime(dt):
    """Format datetime to ISO format"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt

def format_timestamp(timestamp):
    """Format Unix timestamp"""
    return datetime.fromtimestamp(timestamp).isoformat()
