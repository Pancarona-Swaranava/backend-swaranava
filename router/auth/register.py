"""
Register endpoint untuk registrasi user baru
"""

from flask import Blueprint, request, jsonify
from database import db
from models.user import User

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    # Endpoint untuk registrasi user baru
    # Body: { username, email, password, full_name (optional) }
    try:
        data = request.get_json()
        
        # Validasi input
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validasi required fields
        if not username or not email or not password:
            return jsonify({
                'message': 'Username, email, and password are required'
            }), 400
        
        # Validasi panjang password
        if len(password) < 6:
            return jsonify({
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Validasi format email sederhana
        if '@' not in email:
            return jsonify({
                'message': 'Invalid email format'
            }), 400
        
        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            return jsonify({
                'message': 'Username already exists'
            }), 409
        
        # Cek apakah email sudah ada
        if User.query.filter_by(email=email).first():
            return jsonify({
                'message': 'Email already exists'
            }), 409
        
        # Buat user baru
        new_user = User(
            username=username,
            email=email,
            full_name=full_name if full_name else None
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = new_user.generate_token()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Registration failed',
            'error': str(e)
        }), 500