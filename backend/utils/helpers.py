"""Helper utilities"""

def get_page_and_limit(request, default_limit=10, max_limit=100):
    """Extract pagination parameters from request"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', default_limit, type=int)
    limit = min(limit, max_limit)
    return page, limit

def paginate_query(query, page, limit):
    """Paginate a SQLAlchemy query"""
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()
