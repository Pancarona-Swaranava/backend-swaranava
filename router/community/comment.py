"""
Comment endpoints untuk community comments
"""

from flask import Blueprint, request, jsonify
from database import db
from models.community import Comment, Post
from utils.auth import token_required

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@token_required
def get_comments(current_user, post_id):
    # Endpoint untuk mendapatkan semua comments pada post
    # Query params: limit (optional), offset (optional)
    try:
        # Cek apakah post exists
        post = Post.query.get_or_404(post_id)
        
        if not post.is_active:
            return jsonify({'message': 'Post not found'}), 404
        
        limit = request.args.get('limit', type=int, default=50)
        offset = request.args.get('offset', type=int, default=0)
        
        comments = Comment.query.filter_by(
            post_id=post_id,
            is_active=True
        ).order_by(Comment.created_at.asc()).offset(offset).limit(limit).all()
        
        return jsonify({
            'message': 'Comments retrieved successfully',
            'post_id': post_id,
            'comments': [comment.to_dict(include_user=True) for comment in comments],
            'count': len(comments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve comments',
            'error': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['GET'])
@token_required
def get_comment(current_user, comment_id):
    # Endpoint untuk mendapatkan detail comment berdasarkan ID
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        if not comment.is_active:
            return jsonify({'message': 'Comment not found'}), 404
        
        return jsonify({
            'message': 'Comment retrieved successfully',
            'comment': comment.to_dict(include_user=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve comment',
            'error': str(e)
        }), 500


@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, post_id):
    # Endpoint untuk membuat comment baru pada post
    # Body: { content }
    try:
        # Cek apakah post exists
        post = Post.query.get_or_404(post_id)
        
        if not post.is_active:
            return jsonify({'message': 'Post not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({
                'message': 'Content is required'
            }), 400
        
        new_comment = Comment(
            user_id=current_user.id,
            post_id=post_id,
            content=content
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': new_comment.to_dict(include_user=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to create comment',
            'error': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    # Endpoint untuk update comment (hanya pemilik comment)
    # Body: { content }
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        if comment.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        if not comment.is_active:
            return jsonify({'message': 'Comment not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({
                'message': 'Content is required'
            }), 400
        
        comment.content = content
        db.session.commit()
        
        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict(include_user=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to update comment',
            'error': str(e)
        }), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    # Endpoint untuk delete comment (hanya pemilik comment)
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        if comment.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        comment.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Comment deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to delete comment',
            'error': str(e)
        }), 500