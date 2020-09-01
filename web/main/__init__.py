import os
from flask import Flask
from flask_breadcrumbs import Breadcrumbs
from dotenv import load_dotenv
from flask_wtf import CSRFProtect


def create_app():
    webpage = Flask(__name__)
    csrf = CSRFProtect(webpage)
    load_dotenv()
    webpage.config['API_URL'] = os.getenv('API_URL')
    # Gets the backend url and links it to the app's api url
    webpage.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Blueprints import
    from main.routes import admin, login, main, seismologist, unlogged_usr
    webpage.register_blueprint(admin)
    webpage.register_blueprint(login)
    webpage.register_blueprint(main)
    webpage.register_blueprint(seismologist)
    webpage.register_blueprint(unlogged_usr)
    csrf.init_app(webpage)

    return webpage
