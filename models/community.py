"""
Community models untuk Post, Comment, dan Like
"""

from database import db
from datetime import datetime

class Post(db.Model):
    # Model untuk post di community
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    is_pinned = db.Column(db.Boolean, default=False, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='Comment.created_at')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def get_likes_count(self):
        """Hitung jumlah likes - optimasi dengan query langsung"""
        # Gunakan query langsung untuk efisiensi (menghindari lazy load)
        # Import di sini untuk menghindari circular import
        from models.community import Like
        return Like.query.filter_by(post_id=self.id).count()
    
    def get_comments_count(self):
        """Hitung jumlah comments - optimasi dengan query langsung"""
        # Gunakan query langsung untuk efisiensi (hanya count active comments)
        # Import di sini untuk menghindari circular import
        from models.community import Comment
        return Comment.query.filter_by(post_id=self.id, is_active=True).count()
    
    def to_dict(self, include_user=False):
        # Convert model instance ke dictionary
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'is_pinned': self.is_pinned,
            'is_active': self.is_active,
            'likes_count': self.get_likes_count(),
            'comments_count': self.get_comments_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'full_name': self.user.full_name,
                'avatar_url': self.user.avatar_url
            }
        return data
    
    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    # Model untuk comment pada post
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self, include_user=False):
        # Convert model instance ke dictionary
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'full_name': self.user.full_name,
                'avatar_url': self.user.avatar_url
            }
        return data
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class Like(db.Model):
    # Model untuk like pada post
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint: satu user hanya bisa like sekali per post
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)
    
    def to_dict(self):
        """Convert model instance ke dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Like User:{self.user_id} Post:{self.post_id}>'


