# # app/routes/users.py
# from flask import Blueprint, request, jsonify
# from app.models import User
# from app import db
#
# users_bp = Blueprint('users', __name__)
#
# @users_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     email = data.get('email')
#
#     if not username or not password or not email:
#         return jsonify({"msg": "Missing required fields"}), 400
#
#     if User.query.filter_by(username=username).first():
#         return jsonify({"msg": "Username already exists"}), 400
#
#     if User.query.filter_by(email=email).first():
#         return jsonify({"msg": "Email already exists"}), 400
#
#     new_user = User(username=username, password=password, email=email)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return jsonify({"msg": "User registered successfully"}), 201
#
# @users_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     if not username or not password:
#         return jsonify({"msg": "Missing username or password"}), 400
#
#     user = User.query.filter_by(username=username, password=password).first()
#
#     if not user:
#         return jsonify({"msg": "Invalid credentials"}), 401
#
#     # 这里简化了，不使用 JWT，直接返回用户信息
#     return jsonify({
#         "msg": "Login successful",
#         "user": {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "created_at": user.created_at
#         }
#     }), 200
