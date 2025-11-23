"""
User router untuk user profile dan management
"""

from flask import Blueprint
from router.user.profile import profile_bp

# Buat parent blueprint untuk user
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# Register sub-blueprints
user_bp.register_blueprint(profile_bp)


