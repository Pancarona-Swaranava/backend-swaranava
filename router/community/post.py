"""
Post endpoints untuk community posts
"""

from flask import Blueprint, request, jsonify
from database import db
from models.community import Post
from utils.auth import token_required
from sqlalchemy import or_

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    """
    Endpoint untuk mendapatkan semua posts
    Query params: 
        - search (optional): Search di title dan content
        - user_id (optional): Filter posts oleh user tertentu
        - is_pinned (optional): Filter hanya pinned posts (true/false)
        - limit (optional): Jumlah posts per page (default: 20)
        - offset (optional): Offset untuk pagination (default: 0)
    """
    try:
        search = request.args.get('search', '').strip()
        user_id = request.args.get('user_id', type=int)
        is_pinned = request.args.get('is_pinned')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)
        
        # Validasi limit dan offset
        if limit < 1 or limit > 100:
            limit = 20
        if offset < 0:
            offset = 0
        
        # Query dasar: hanya posts yang aktif
        query = Post.query.filter_by(is_active=True)
        
        # Filter berdasarkan user_id
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Filter berdasarkan is_pinned
        if is_pinned is not None:
            is_pinned_bool = is_pinned.lower() == 'true'
            query = query.filter_by(is_pinned=is_pinned_bool)
        
        # Search di title dan content
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern)
                )
            )
        
        # Sort: pinned posts dulu, kemudian by created_at desc
        posts = query.order_by(
            Post.is_pinned.desc(),
            Post.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        # Hitung total posts untuk pagination info
        total_count = query.count()
        
        return jsonify({
            'message': 'Posts retrieved successfully',
            'posts': [post.to_dict(include_user=True) for post in posts],
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': (offset + limit) < total_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve posts',
            'error': str(e)
        }), 500


@post_bp.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(current_user, post_id):
    # Endpoint untuk mendapatkan detail post berdasarkan ID
    try:
        post = Post.query.get_or_404(post_id)
        
        # Cek apakah post aktif
        if not post.is_active:
            return jsonify({
                'message': 'Post not found'
            }), 404
        
        return jsonify({
            'message': 'Post retrieved successfully',
            'post': post.to_dict(include_user=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve post',
            'error': str(e)
        }), 500


@post_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    """
    Endpoint untuk membuat post baru
    Body: 
        - title (required): Judul post
        - content (required): Isi/konten post
        - image_url (optional): URL gambar untuk post
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'message': 'No data provided'
            }), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        image_url = data.get('image_url', '').strip()
        
        # Validasi required fields
        if not title:
            return jsonify({
                'message': 'Title is required'
            }), 400
        
        if not content:
            return jsonify({
                'message': 'Content is required'
            }), 400
        
        # Validasi panjang title
        if len(title) > 200:
            return jsonify({
                'message': 'Title must be 200 characters or less'
            }), 400
        
        # Buat post baru
        new_post = Post(
            user_id=current_user.id,
            title=title,
            content=content,
            image_url=image_url if image_url else None
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': new_post.to_dict(include_user=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to create post',
            'error': str(e)
        }), 500


@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """
    Endpoint untuk update post (hanya pemilik post yang bisa update)
    Body:
        - title (optional): Judul post baru
        - content (optional): Konten post baru
        - image_url (optional): URL gambar baru (bisa null untuk hapus)
    """
    try:
        post = Post.query.get_or_404(post_id)
        
        # Cek apakah post aktif
        if not post.is_active:
            return jsonify({
                'message': 'Post not found'
            }), 404
        
        # Cek apakah user adalah pemilik post
        if post.user_id != current_user.id:
            return jsonify({
                'message': 'Unauthorized: You can only update your own posts'
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'message': 'No data provided'
            }), 400
        
        # Update title jika diberikan
        if 'title' in data:
            new_title = data['title'].strip() if data['title'] else ''
            if not new_title:
                return jsonify({
                    'message': 'Title cannot be empty'
                }), 400
            if len(new_title) > 200:
                return jsonify({
                    'message': 'Title must be 200 characters or less'
                }), 400
            post.title = new_title
        
        # Update content jika diberikan
        if 'content' in data:
            new_content = data['content'].strip() if data['content'] else ''
            if not new_content:
                return jsonify({
                    'message': 'Content cannot be empty'
                }), 400
            post.content = new_content
        
        # Update image_url jika diberikan
        if 'image_url' in data:
            post.image_url = data['image_url'].strip() if data['image_url'] else None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict(include_user=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to update post',
            'error': str(e)
        }), 500


@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    # sEndpoint untuk delete post (soft delete - hanya pemilik post yang bisa delete)
    # Post tidak akan benar-benar dihapus, hanya di-mark sebagai tidak aktif
    try:
        post = Post.query.get_or_404(post_id)
        
        # Cek apakah post aktif
        if not post.is_active:
            return jsonify({
                'message': 'Post not found'
            }), 404
        
        # Cek apakah user adalah pemilik post
        if post.user_id != current_user.id:
            return jsonify({
                'message': 'Unauthorized: You can only delete your own posts'
            }), 403
        
        # Soft delete: set is_active = False
        post.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Post deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to delete post',
            'error': str(e)
        }), 500


@post_bp.route('/posts/<int:post_id>/pin', methods=['POST'])
@token_required
def pin_post(current_user, post_id):
    """
    Endpoint untuk pin/unpin post (hanya pemilik post yang bisa)
    Body:
        - is_pinned (optional): true untuk pin, false untuk unpin (default: true)
    """
    try:
        post = Post.query.get_or_404(post_id)
        
        # Cek apakah post aktif
        if not post.is_active:
            return jsonify({
                'message': 'Post not found'
            }), 404
        
        # Cek apakah user adalah pemilik post
        if post.user_id != current_user.id:
            return jsonify({
                'message': 'Unauthorized: You can only pin your own posts'
            }), 403
        
        data = request.get_json() or {}
        is_pinned = data.get('is_pinned', True)
        
        post.is_pinned = bool(is_pinned)
        db.session.commit()
        
        action = 'pinned' if is_pinned else 'unpinned'
        
        return jsonify({
            'message': f'Post {action} successfully',
            'post': post.to_dict(include_user=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to pin/unpin post',
            'error': str(e)
        }), 500
