# backend/app/routes/modules.py

from flask import Blueprint, request, jsonify
from ..models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('modules', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not all([username, password, email]):
        return jsonify({'message': '缺少必要参数'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': '电子邮件已存在'}), 400

    new_user = User(
        username=username,
        password=password,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'message': '缺少必要参数'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not password:
        return jsonify({'message': '用户名或密码错误'}), 401

    # 这里可以生成并返回JWT令牌，简化起见暂不实现
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }

    return jsonify({'message': 'success', 'user': user_data}), 200
