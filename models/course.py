"""
Course dan Level models untuk learning system
"""

from database import db
from datetime import datetime

class Course(db.Model):
    # Model untuk course/kelas pembelajaran
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    difficulty_level = db.Column(db.String(20), nullable=False, default='beginner', index=True)  # beginner, intermediate, advanced
    estimated_duration = db.Column(db.Integer, nullable=True)  # dalam menit
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    levels = db.relationship('Level', backref='course', lazy=True, cascade='all, delete-orphan', order_by='Level.order_number')
    progress = db.relationship('Progress', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        # Convert model instance ke dictionary
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'difficulty_level': self.difficulty_level,
            'estimated_duration': self.estimated_duration,
            'is_active': self.is_active,
            'levels_count': len(self.levels) if self.levels else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Course {self.title}>'


class Level(db.Model):
    # Model untuk level/tingkat dalam course
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # Konten pembelajaran
    order_number = db.Column(db.Integer, nullable=False, default=1)  # Urutan level dalam course
    video_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    progress = db.relationship('Progress', backref='level', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        # Convert model instance ke dictionary
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'order_number': self.order_number,
            'video_url': self.video_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Level {self.title}>'


