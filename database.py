"""
Konfigurasi dan setup database menggunakan SQLAlchemy ORM
Menggunakan MySQL sebagai database
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.exc import OperationalError
import os
import sys

# Inisialisasi SQLAlchemy instance
db = SQLAlchemy()

def init_db(app: Flask):
    """
    Inisialisasi database dengan Flask app
    
    Args:
        app: Flask application instance
    
    Raises:
        SystemExit: Jika koneksi database gagal dan SKIP_DB_INIT tidak di-set
    """
    # Konfigurasi database URI dari environment variable atau default
    # Format: mysql+pymysql://username:password@host:port/database_name
    database_uri = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://swaranava_user:password@localhost:3306/swaranava_db'
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Inisialisasi database dengan app
    db.init_app(app)
    
    # Buat semua tabel jika belum ada (hanya untuk development)
    # Catch error jika database connection gagal
    skip_db_init = os.getenv('SKIP_DB_INIT', 'False').lower() == 'true'
    
    if not skip_db_init:
        try:
            with app.app_context():
                # Test koneksi database terlebih dahulu
                db.engine.connect()
                print("✓ Database connection successful")
                
                # Buat semua tabel jika belum ada
                db.create_all()
                print("✓ Database tables initialized")
                
        except OperationalError as e:
            error_msg = str(e)
            print("\n" + "="*70)
            print("ERROR: Database connection failed!")
            print("="*70)
            print(f"\nError details: {error_msg}\n")
            
            # Parse error untuk memberikan saran yang lebih baik
            if "Access denied" in error_msg:
                print("Possible solutions:")
                print("1. Check database credentials in DATABASE_URI environment variable")
                print("2. Ensure the database user has proper permissions:")
                print("   GRANT ALL PRIVILEGES ON swaranava_db.* TO 'user'@'localhost';")
                print("   FLUSH PRIVILEGES;")
                print("3. Verify the database exists:")
                print("   CREATE DATABASE swaranava_db;")
            elif "Unknown database" in error_msg:
                print("Possible solutions:")
                print("1. Create the database first:")
                print("   CREATE DATABASE swaranava_db;")
                print("2. Update DATABASE_URI to point to an existing database")
            elif "Can't connect" in error_msg:
                print("Possible solutions:")
                print("1. Ensure MySQL server is running")
                print("2. Check host and port in DATABASE_URI")
                print("3. Verify network connectivity")
            
            print(f"\nSet SKIP_DB_INIT=true to skip database initialization")
            print("="*70 + "\n")
            
            # Hanya exit jika bukan development mode dengan skip flag
            if os.getenv('FLASK_ENV') != 'development' and not skip_db_init:
                sys.exit(1)
        except Exception as e:
            print(f"\n⚠ Warning: Database initialization failed: {str(e)}")
            print("Server will continue but database operations may fail.\n")
    else:
        print("⚠ Skipping database initialization (SKIP_DB_INIT=true)")

def get_db():
    """
    Mendapatkan database instance
    
    Returns:
        SQLAlchemy database instance
    """
    return db

