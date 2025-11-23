"""
Learning router untuk course, level, dan progress endpoints
"""

from flask import Blueprint
from router.learning.course import course_bp
from router.learning.progress import progress_bp
from router.learning.level import level_bp

# Buat parent blueprint untuk learning
learning_bp = Blueprint('learning', __name__, url_prefix='/api/learning')

# Register sub-blueprints
learning_bp.register_blueprint(course_bp)
learning_bp.register_blueprint(progress_bp)
learning_bp.register_blueprint(level_bp)


