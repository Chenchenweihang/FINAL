# backend/app/routes/auth.py

from flask import Blueprint, request, jsonify
from ..models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # 注意：生产环境请使用哈希加密
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'message': '缺少必要参数'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': '电子邮件已存在'}), 400

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '缺少必要参数'}), 400

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({'message': '用户名或密码错误'}), 401

    # 简单返回用户信息，生产环境请使用认证令牌
    return jsonify({
        'message': '登录成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
    }), 200
