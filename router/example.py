"""
Contoh modul router
File ini dapat dijadikan template untuk membuat modul router baru
"""

from flask import Blueprint, jsonify

example_bp = Blueprint('example', __name__)

@example_bp.route('/test', methods=['GET'])
def test_endpoint():
    """
    Contoh endpoint untuk testing
    """
    return jsonify({
        'message': 'Test endpoint berhasil',
        'status': 'success'
    }), 200

# Untuk menggunakan modul ini, import di router/__init__.py:
# from router.example import example_bp
# app.register_blueprint(example_bp, url_prefix='/api/example')