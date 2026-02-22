"""Application constants"""

SCHOOL_NAME = "Kellyville Ridge Public School"
SCHOOL_CODE = "KRPS"
KRPS_GREEN = "#2D8B3D"

# Tiers
TIERS = {
    'mild': 'Mild (Working Towards)',
    'medium': 'Medium (Working At Grade Level)',
    'spicy': 'Spicy (Working Above)',
    'enrichment': 'Enrichment (Extension)'
}

# JWT Settings
JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days

# Database
DATABASE_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
