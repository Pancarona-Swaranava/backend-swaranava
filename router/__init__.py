"""
Router module untuk mengorganisir semua API routes
Semua routes dipecah menjadi beberapa modul sesuai kebutuhan
"""

from router.auth import auth_bp
from router.learning import learning_bp
from router.community import community_bp
from router.user import user_bp

def register_routes(app):
    """
    Fungsi untuk mendaftarkan semua routes ke Flask app
    
    Args:
        app: Flask application instance
    """
    # Register semua blueprint ke app
    app.register_blueprint(auth_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(user_bp)