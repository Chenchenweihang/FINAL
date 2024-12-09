# backend/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化插件
    db.init_app(app)
    jwt.init_app(app)

    # 配置 CORS，允许所有来源跨域请求
    CORS(app, supports_credentials=True)

    # 导入并注册蓝图
    from .routes import main_bp  # 使用相对导入
    app.register_blueprint(main_bp, url_prefix='/api')

    # 创建数据库表（如果尚未创建）
    with app.app_context():
        db.create_all()

    return app
