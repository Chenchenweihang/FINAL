# backend/app/__init__.py

from flask import Flask
from .models import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.characters import characters_bp
    from .routes.skills import skills_bp
    from .routes.maps import maps_bp
    from .routes.tasks import tasks_bp
    from .routes.inventory import inventory_bp
    from .routes.battles import battles_bp
    from .routes.items import items_bp
    from .routes.events import events_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(skills_bp, url_prefix='/skills')
    app.register_blueprint(maps_bp, url_prefix='/maps')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(battles_bp, url_prefix='/battles')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(events_bp, url_prefix='/events')

    return app
