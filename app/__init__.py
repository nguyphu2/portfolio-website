# app/__init__.py - Flask application factory
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    from app.routes.public import public
    from app.routes.admin import admin
    app.register_blueprint(public)
    app.register_blueprint(admin)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))
