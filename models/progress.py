"""
Progress model untuk tracking pembelajaran user
"""

from database import db
from datetime import datetime

class Progress(db.Model):
    # Model untuk tracking progress user dalam course dan level
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id', ondelete='CASCADE'), nullable=True, index=True)
    status = db.Column(db.String(20), nullable=False, default='not_started', index=True)  # not_started, in_progress, completed
    completion_percentage = db.Column(db.Float, default=0.0, nullable=False)  # 0-100
    last_accessed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint: satu user hanya punya satu progress per course
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_user_course_progress'),)
    
    def to_dict(self):
        # Convert model instance ke dictionary
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'level_id': self.level_id,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Progress User:{self.user_id} Course:{self.course_id}>'


