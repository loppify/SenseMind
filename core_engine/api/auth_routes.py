from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from core_engine.database.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          properties:
            username: {type: string}
            email: {type: string}
            password: {type: string}
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() or \
       User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created", "user_id": user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          properties:
            username: {type: string}
            password: {type: string}
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, username=user.username), 200
    return jsonify({"msg": "Bad username or password"}), 401
