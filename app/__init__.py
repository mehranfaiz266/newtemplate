import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from cryptography.fernet import Fernet


db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY', 'change_this'),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            ENCRYPTION_KEY=os.getenv('ENCRYPTION_KEY')
        )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        from . import routes, models  # noqa
        db.create_all()

    return app


def get_fernet(app):
    key = app.config.get('ENCRYPTION_KEY')
    if not key:
        secret = app.config['SECRET_KEY']
        key = Fernet.generate_key()
        app.config['ENCRYPTION_KEY'] = key
    return Fernet(key)
