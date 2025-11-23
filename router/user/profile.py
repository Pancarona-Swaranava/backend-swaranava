"""
Profile endpoints untuk user profile management
"""

from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from utils.auth import token_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    # Endpoint untuk mendapatkan profile user yang sedang login
    try:
        return jsonify({
            'message': 'Profile retrieved successfully',
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve profile',
            'error': str(e)
        }), 500


@profile_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    # Endpoint untuk update profile user
    # Body: { full_name, bio, avatar_url (optional) }
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Update fields yang diizinkan
        if 'full_name' in data:
            current_user.full_name = data['full_name'].strip() if data['full_name'] else None
        
        if 'bio' in data:
            current_user.bio = data['bio'].strip() if data['bio'] else None
        
        if 'avatar_url' in data:
            current_user.avatar_url = data['avatar_url'].strip() if data['avatar_url'] else None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to update profile',
            'error': str(e)
        }), 500


@profile_bp.route('/profile/change-name', methods=['PUT'])
@token_required
def change_name(current_user):
    # Endpoint khusus untuk change name
    # Body: { full_name }
    try:
        data = request.get_json()
        
        if not data or 'full_name' not in data:
            return jsonify({'message': 'full_name is required'}), 400
        
        full_name = data['full_name'].strip()
        
        if not full_name:
            return jsonify({'message': 'full_name cannot be empty'}), 400
        
        current_user.full_name = full_name
        db.session.commit()
        
        return jsonify({
            'message': 'Name changed successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to change name',
            'error': str(e)
        }), 500


