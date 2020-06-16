import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    # Gets the backend url and links it to the app's api url

    # Blueprints import
    # from main.routes import main, login, users, sensors, verified_seisms, unverified_seisms
    # app.register_blueprint(routes.main.main) .. and so on

    return app
