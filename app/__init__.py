# app/__init__.py - Flask application factory
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    limiter.init_app(app)

    from app.routes.public import public
    from app.routes.admin import admin
    app.register_blueprint(public)
    app.register_blueprint(admin)

    from flask import redirect, url_for, flash

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        flash("You've sent a few messages already - please try again in a bit.")
        return redirect(url_for('public.contact'))

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))
