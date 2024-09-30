from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import User
from app import db, bcrypt
from flask_jwt_extended import create_access_token
from app.serializers import UserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify(UserSchema().dump(user)), 201

@auth_bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users)), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    user.login_dt = datetime.now()
    db.session.add(user)
    db.session.commit()


    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

