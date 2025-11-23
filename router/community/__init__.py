"""
Community router untuk post, comment, dan like endpoints
"""

from flask import Blueprint
from router.community.post import post_bp
from router.community.comment import comment_bp
from router.community.like import like_bp

# Buat parent blueprint untuk community
community_bp = Blueprint('community', __name__, url_prefix='/api/community')

# Register sub-blueprints
community_bp.register_blueprint(post_bp)
community_bp.register_blueprint(comment_bp)
community_bp.register_blueprint(like_bp)


