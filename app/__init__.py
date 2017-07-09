# app/__init__.py
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_babel import Babel, gettext
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import LANGUAGES,app_config


bootstrap = Bootstrap()
babel = Babel()
mail = Mail()
db= SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    bootstrap.init_app(app)
    #db.init_app(app)
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())

    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app