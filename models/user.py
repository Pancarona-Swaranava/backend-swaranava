"""
User model untuk autentikasi dan profil user
"""

from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os

class User(db.Model):
    # Model untuk user dengan autentikasi
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        # Hash password dan simpa
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # Verifikasi password
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        # Generate JWT token untuk user
        secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.utcnow().timestamp() + 86400  # 24 hours
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def to_dict(self, include_sensitive=False):
        # Convert model instance ke dictionary
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'


