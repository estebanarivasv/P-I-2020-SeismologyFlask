import os
from flask import Flask, flash, redirect, url_for
from dotenv import load_dotenv

from main.extensions import login_manager, csrf
from main.routes import auth, main, user

@login_manager.unauthorized_handler
def unauthorized_callback():
    # Shows to user a pop up saying that they are not allowed to access to that url route. Redirects to login form
    flash("You must sign up before continuing", "warning")
    return redirect(url_for('auth.login'))

def create_app():
    webpage = Flask(__name__)
    load_dotenv()

    webpage.config['API_URL'] = os.getenv('API_URL')
    webpage.config['SECRET_KEY'] = os.getenv('SECRET_KEY')    

    # Importing blueprints
    webpage.register_blueprint(auth)
    webpage.register_blueprint(main)
    webpage.register_blueprint(user)

    csrf.init_app(webpage)
    login_manager.init_app(webpage)

    return webpage
