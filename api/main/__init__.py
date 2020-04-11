import os

from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()


import main.resources


def create_app():
    app = Flask(__name__)

    load_dotenv()

    if not os.path.exists(os.getenv('SQLALCHEMY_DB_PATH') + os.getenv('SQLALCHEMY_DB_NAME')):
        os.mknod(os.getenv('SQLALCHEMY_DB_PATH') + os.getenv('SQLALCHEMY_DB_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + str(os.getenv('SQLALCHEMY_DB_PATH')) + str(os.getenv('SQLALCHEMY_DB_NAME'))

    db.init_app(app)

    api.add_resource(resources.SensorResource, '/sensor/<id_num>')
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.UnverifiedSeismResource, '/unverified-seism/<id_num>')
    api.add_resource(resources.UnverifiedSeismsResource, '/unverified-seisms')
    api.add_resource(resources.VerifiedSeismResource, '/verified-seism/<id_num>')
    api.add_resource(resources.VerifiedSeismsResource, '/verified-seisms')
    api.add_resource(resources.UserResource, '/user/<id_num>')
    api.add_resource(resources.UsersResource, '/users')

    api.init_app(app)

    return app

