"""
Server utama untuk aplikasi Swaranava Backend
Menggunakan Flask sebagai framework web
"""

from flask import Flask, jsonify
from flask_cors import CORS
from router import register_routes
from database import init_db
import sys
import os

# Inisialisasi Flask app
app = Flask(__name__)

# Enable CORS untuk komunikasi dengan frontend Next.js
CORS(app)

# Inisialisasi database
# Database initialization akan handle error sendiri dan print pesan yang informatif
try:
    init_db(app)
except SystemExit:
    # Jika database init gagal dan exit dipanggil, tangkap di sini
    # Server tetap bisa berjalan jika SKIP_DB_INIT=true
    skip_db_init = os.getenv('SKIP_DB_INIT', 'False').lower() == 'true'
    if not skip_db_init:
        print("\n❌ Database initialization failed. Server cannot start without database.")
        print("Set SKIP_DB_INIT=true environment variable to continue without database.\n")
        sys.exit(1)

# Register semua routes dari router
register_routes(app)

@app.route('/')
def health_check():
    """Endpoint untuk health check"""
    try:
        from database import db
        # Test database connection
        db.engine.connect()
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'ok',
        'message': 'Swaranava Backend API is running',
        'database': db_status
    }), 200

if __name__ == '__main__':
    # Jalankan server Flask
    # Development mode: debug=True
    print("\n" + "="*70)
    print("Swaranava Backend API Server")
    print("="*70)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Database URI: {os.getenv('DATABASE_URI', 'Using default (root:password@localhost/swaranava_db)')}")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

