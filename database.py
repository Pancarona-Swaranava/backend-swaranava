"""
Konfigurasi dan setup database menggunakan SQLAlchemy ORM
Menggunakan MySQL sebagai database
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

# Inisialisasi SQLAlchemy instance
db = SQLAlchemy()

def init_db(app: Flask):
    """
    Inisialisasi database dengan Flask app
    
    Args:
        app: Flask application instance
    """
    # Konfigurasi database URI dari environment variable atau default
    # Format: mysql+pymysql://username:password@host:port/database_name
    database_uri = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://root:password@localhost:3306/swaranava_db'
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Inisialisasi database dengan app
    db.init_app(app)
    
    # Buat semua tabel jika belum ada (hanya untuk development)
    with app.app_context():
        db.create_all()

def get_db():
    """
    Mendapatkan database instance
    
    Returns:
        SQLAlchemy database instance
    """
    return db

