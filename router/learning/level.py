"""
Level endpoints untuk mendapatkan level dalam course
"""

from flask import Blueprint, request, jsonify
from models.course import Level, Course
from utils.auth import token_required

level_bp = Blueprint('level', __name__)

@level_bp.route('/courses/<int:course_id>/levels', methods=['GET'])
@token_required
def get_levels(current_user, course_id):
    # Endpoint untuk mendapatkan semua levels dalam course
    try:
        # Cek apakah course exists
        course = Course.query.get_or_404(course_id)
        
        levels = Level.query.filter_by(
            course_id=course_id,
            is_active=True
        ).order_by(Level.order_number).all()
        
        return jsonify({
            'message': 'Levels retrieved successfully',
            'course_id': course_id,
            'levels': [level.to_dict() for level in levels],
            'count': len(levels)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve levels',
            'error': str(e)
        }), 500


@level_bp.route('/levels/<int:level_id>', methods=['GET'])
@token_required
def get_level(current_user, level_id):
    # Endpoint untuk mendapatkan detail level berdasarkan ID
    try:
        level = Level.query.get_or_404(level_id)
        
        return jsonify({
            'message': 'Level retrieved successfully',
            'level': level.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve level',
            'error': str(e)
        }), 500


