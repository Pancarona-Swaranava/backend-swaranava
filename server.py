"""
Server utama untuk aplikasi Swaranava Backend
Menggunakan Flask sebagai framework web
"""

from flask import Flask
from flask_cors import CORS
from router import register_routes

# Inisialisasi Flask app
app = Flask(__name__)

# Enable CORS untuk komunikasi dengan frontend Next.js
CORS(app)

# Register semua routes dari router
register_routes(app)

@app.route('/')
def health_check():
    """Endpoint untuk health check"""
    return {
        'status': 'ok',
        'message': 'Swaranava Backend API is running'
    }, 200

if __name__ == '__main__':
    # Jalankan server Flask
    # Development mode: debug=True
    app.run(debug=True, host='0.0.0.0', port=5000)

