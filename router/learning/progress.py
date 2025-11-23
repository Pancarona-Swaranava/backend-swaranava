"""
Progress endpoints untuk tracking pembelajaran user
"""

from flask import Blueprint, request, jsonify
from database import db
from models.progress import Progress
from models.course import Course, Level
from utils.auth import token_required
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress', methods=['GET'])
@token_required
def get_user_progress(current_user):
    # Endpoint untuk mendapatkan semua progress user
    # Query params: course_id (optional)
    try:
        course_id = request.args.get('course_id', type=int)
        
        query = Progress.query.filter_by(user_id=current_user.id)
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        progress_list = query.order_by(Progress.updated_at.desc()).all()
        
        return jsonify({
            'message': 'Progress retrieved successfully',
            'progress': [p.to_dict() for p in progress_list],
            'count': len(progress_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve progress',
            'error': str(e)
        }), 500


@progress_bp.route('/progress/course/<int:course_id>', methods=['GET'])
@token_required
def get_course_progress(current_user, course_id):
    # Endpoint untuk mendapatkan progress user pada course tertentu
    try:
        # Cek apakah course exists
        Course.query.get_or_404(course_id)
        
        progress = Progress.query.filter_by(
            user_id=current_user.id,
            course_id=course_id
        ).first()
        
        if not progress:
            return jsonify({
                'message': 'No progress found for this course',
                'progress': None
            }), 200
        
        return jsonify({
            'message': 'Progress retrieved successfully',
            'progress': progress.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve progress',
            'error': str(e)
        }), 500


@progress_bp.route('/progress', methods=['POST'])
@token_required
def create_or_update_progress(current_user):
    # Endpoint untuk membuat atau update progress
    # Body: { course_id, level_id (optional), status, completion_percentage }
    try:
        data = request.get_json()
        
        if not data or 'course_id' not in data:
            return jsonify({'message': 'course_id is required'}), 400
        
        course_id = data['course_id']
        level_id = data.get('level_id')
        status = data.get('status', 'in_progress')
        completion_percentage = data.get('completion_percentage', 0.0)
        
        # Validasi status
        if status not in ['not_started', 'in_progress', 'completed']:
            return jsonify({'message': 'Invalid status'}), 400
        
        # Validasi completion_percentage
        if not 0 <= completion_percentage <= 100:
            return jsonify({'message': 'completion_percentage must be between 0 and 100'}), 400
        
        # Cek apakah course exists
        Course.query.get_or_404(course_id)
        
        # Cek apakah level exists jika level_id diberikan
        if level_id:
            Level.query.get_or_404(level_id)
        
        # Cari atau buat progress
        progress = Progress.query.filter_by(
            user_id=current_user.id,
            course_id=course_id
        ).first()
        
        if progress:
            # Update existing progress
            progress.level_id = level_id if level_id else progress.level_id
            progress.status = status
            progress.completion_percentage = completion_percentage
            progress.last_accessed_at = datetime.utcnow()
            
            if status == 'completed' and not progress.completed_at:
                progress.completed_at = datetime.utcnow()
            elif status != 'completed':
                progress.completed_at = None
        else:
            # Buat progress baru
            progress = Progress(
                user_id=current_user.id,
                course_id=course_id,
                level_id=level_id,
                status=status,
                completion_percentage=completion_percentage
            )
            db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress saved successfully',
            'progress': progress.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to save progress',
            'error': str(e)
        }), 500