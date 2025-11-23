"""
Course endpoints untuk mendapatkan dan mengelola course
"""

from flask import Blueprint, request, jsonify
from models.course import Course
from utils.auth import token_required

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    # Endpoint untuk mendapatkan semua courses
    # Query params: difficulty_level (optional), is_active (optional)
    try:
        difficulty_level = request.args.get('difficulty_level')
        is_active = request.args.get('is_active', 'true').lower() == 'true'
        
        query = Course.query.filter_by(is_active=is_active)
        
        if difficulty_level:
            query = query.filter_by(difficulty_level=difficulty_level)
        
        courses = query.order_by(Course.created_at.desc()).all()
        
        return jsonify({
            'message': 'Courses retrieved successfully',
            'courses': [course.to_dict() for course in courses],
            'count': len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve courses',
            'error': str(e)
        }), 500


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
@token_required
def get_course(current_user, course_id):
    # Endpoint untuk mendapatkan detail course berdasarkan ID
    try:
        course = Course.query.get_or_404(course_id)
        
        course_dict = course.to_dict()
        # Tambahkan levels ke response
        course_dict['levels'] = [level.to_dict() for level in course.levels if level.is_active]
        
        return jsonify({
            'message': 'Course retrieved successfully',
            'course': course_dict
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve course',
            'error': str(e)
        }), 500


