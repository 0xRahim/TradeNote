from flask import Blueprint, request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from flask import current_app
from app.utils.auth import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password, avatar=data.get('avatar'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return jsonify({'message': 'Could not verify'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'message': 'Could not verify'}), 401

@auth_bp.route('/avatar', methods=['POST'])
@token_required
def upload_avatar(current_user):
    data = request.get_json()
    if 'avatar' not in data:
        return jsonify({'message': 'No avatar data'}), 400
    current_user.avatar = data['avatar']
    db.session.commit()
    return jsonify({'message': 'Avatar updated!'})

@auth_bp.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    user_data = {}
    user_data['id'] = current_user.id
    user_data['username'] = current_user.username
    user_data['avatar'] = current_user.avatar
    return jsonify(user_data)
