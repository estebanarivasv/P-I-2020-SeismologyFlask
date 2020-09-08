import os
from flask import Flask, flash, redirect, url_for
from flask_breadcrumbs import Breadcrumbs
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager

login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.unauthorized_handler
def unauthorized_callback():
    # Shows to user a pop up saying that they are not allowed to access to that url route. Redirects to login form
    flash("You must sign up before continuing", "warning")
    return redirect(url_for('auth.login'))

def create_app():
    webpage = Flask(__name__)
    load_dotenv()

    webpage.config['API_URL'] = os.getenv('API_URL')  # Gets the backend url and links it to the app's api url
    webpage.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Blueprints import
    from main.routes import admin, auth, main, seismologist, unlogged_usr
    webpage.register_blueprint(admin)
    webpage.register_blueprint(auth)
    webpage.register_blueprint(main)
    webpage.register_blueprint(seismologist)
    webpage.register_blueprint(unlogged_usr)

    csrf.init_app(webpage)
    login_manager.init_app(webpage)

    return webpage
