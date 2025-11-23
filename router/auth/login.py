"""
Login endpoint untuk autentikasi user
"""

from flask import Blueprint, request, jsonify
from models.user import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    # Endpoint untuk login user
    # Body: { username/email, password }
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        identifier = data.get('username', '').strip() or data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not identifier or not password:
            return jsonify({
                'message': 'Username/email and password are required'
            }), 400
        
        # Cari user berdasarkan username atau email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
        
        if not user:
            return jsonify({
                'message': 'Invalid username/email or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'message': 'Account is deactivated'
            }), 403
        
        # Verifikasi password
        if not user.check_password(password):
            return jsonify({
                'message': 'Invalid username/email or password'
            }), 401
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Login failed',
            'error': str(e)
        }), 500


