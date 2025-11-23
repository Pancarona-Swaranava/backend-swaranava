"""
Models module untuk semua database models
Semua model database didefinisikan di sini
"""

from database import db

# Import semua models
from models.user import User
from models.course import Course, Level
from models.progress import Progress
from models.community import Post, Comment, Like

# Export semua models
__all__ = [
    'db',
    'User',
    'Course',
    'Level',
    'Progress',
    'Post',
    'Comment',
    'Like'
]

