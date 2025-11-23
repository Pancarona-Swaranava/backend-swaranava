"""
Like endpoints untuk community likes
"""

from flask import Blueprint, request, jsonify
from database import db
from models.community import Like, Post
from utils.auth import token_required
from sqlalchemy.exc import IntegrityError

like_bp = Blueprint('like', __name__)

@like_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@token_required
def toggle_like(current_user, post_id):
    # Endpoint untuk like/unlike post
    # Jika sudah like, akan unlike. Jika belum like, akan like.
    try:
        # Cek apakah post exists
        post = Post.query.get_or_404(post_id)
        
        if not post.is_active:
            return jsonify({'message': 'Post not found'}), 404
        
        # Cek apakah user sudah like post ini
        existing_like = Like.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first()
        
        if existing_like:
            # Unlike: hapus like
            db.session.delete(existing_like)
            db.session.commit()
            
            # Refresh post untuk mendapatkan count terbaru
            db.session.refresh(post)
            
            return jsonify({
                'message': 'Post unliked successfully',
                'liked': False,
                'likes_count': post.get_likes_count()
            }), 200
        else:
            # Like: tambahkan like baru
            new_like = Like(
                user_id=current_user.id,
                post_id=post_id
            )
            
            db.session.add(new_like)
            db.session.commit()
            
            # Refresh post untuk mendapatkan count terbaru
            db.session.refresh(post)
            
            return jsonify({
                'message': 'Post liked successfully',
                'liked': True,
                'likes_count': post.get_likes_count()
            }), 201
            
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to like/unlike post',
            'error': 'Duplicate like detected'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to like/unlike post',
            'error': str(e)
        }), 500


@like_bp.route('/posts/<int:post_id>/like/status', methods=['GET'])
@token_required
def get_like_status(current_user, post_id):
    # Endpoint untuk cek apakah user sudah like post ini
    try:
        # Cek apakah post exists
        post = Post.query.get_or_404(post_id)
        
        if not post.is_active:
            return jsonify({'message': 'Post not found'}), 404
        
        # Cek apakah user sudah like post ini
        existing_like = Like.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first()
        
        return jsonify({
            'message': 'Like status retrieved successfully',
            'post_id': post_id,
            'liked': existing_like is not None,
            'likes_count': post.get_likes_count()
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to get like status',
            'error': str(e)
        }), 500


@like_bp.route('/posts/<int:post_id>/likes', methods=['GET'])
@token_required
def get_post_likes(current_user, post_id):
    # Endpoint untuk mendapatkan semua likes pada post
    # Query params: limit (optional), offset (optional)
    try:
        # Cek apakah post exists
        post = Post.query.get_or_404(post_id)
        
        if not post.is_active:
            return jsonify({'message': 'Post not found'}), 404
        
        limit = request.args.get('limit', type=int, default=50)
        offset = request.args.get('offset', type=int, default=0)
        
        likes = Like.query.filter_by(post_id=post_id).order_by(
            Like.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return jsonify({
            'message': 'Likes retrieved successfully',
            'post_id': post_id,
            'likes': [like.to_dict() for like in likes],
            'likes_count': post.get_likes_count(),
            'count': len(likes)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve likes',
            'error': str(e)
        }), 500

