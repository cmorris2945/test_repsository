from flask import Flask
from user_db import init_user_db, db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    
    # Initialize user database
    init_user_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth'

    return app, login_manager, db