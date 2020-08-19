import os
from flask import Flask
from flask_breadcrumbs import Breadcrumbs
from dotenv import load_dotenv
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    # Gets the backend url and links it to the app's api url
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    csrf = CSRFProtect(app)

    # Blueprints import
    from main.routes import admin, login, main, seismologist, unlogged_usr
    app.register_blueprint(admin)
    app.register_blueprint(login)
    app.register_blueprint(main)
    app.register_blueprint(seismologist)
    app.register_blueprint(unlogged_usr)

    return app