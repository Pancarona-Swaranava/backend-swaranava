"""
Auth router untuk authentication endpoints
"""

from flask import Blueprint
from router.auth.login import login_bp
from router.auth.register import register_bp

# Buat parent blueprint untuk auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Register sub-blueprints
auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(register_bp)


