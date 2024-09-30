from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import BlogPost, User
from app import db
from app.serializers import BlogPostSchema, UserSchema

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/create', methods=['POST'])
@jwt_required()
def create_blog():
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')

    user_id = get_jwt_identity()
    blog = BlogPost(title=title, body=body, user_id=user_id)
    db.session.add(blog)
    db.session.commit()

    return BlogPostSchema().jsonify(blog), 201

@blog_bp.route('/all', methods=['GET'])
def get_all_blogs():
    blogs = BlogPost.query.all()
    return BlogPostSchema(many=True).jsonify(blogs), 200

@blog_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_blogs(user_id):
    blogs = BlogPost.query.filter_by(user_id=user_id).all()
    return BlogPostSchema(many=True).jsonify(blogs), 200

@blog_bp.route('/profile', methods=['GET'])
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    blogs = BlogPost.query.filter_by(user_id=user_id).all()
    user_schema = UserSchema()
    blog_schema = BlogPostSchema(many=True)

    return jsonify({
        "user": user_schema.dump(user),
        "blogs": blog_schema.dump(blogs)
    }), 200
