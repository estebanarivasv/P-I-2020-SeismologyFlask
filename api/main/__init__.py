import os

from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

api = Api()
db = SQLAlchemy()
jwt = JWTManager()

import main.resources


def activate_primary_keys(connection, connection_record):
    connection.execute('pragma foreign_keys=ON')


def create_app():
    app = Flask(__name__)

    load_dotenv()

    db_path = str(os.getenv('SQLALCHEMY_DB_PATH'))
    db_name = str(os.getenv('SQLALCHEMY_DB_NAME'))

    if not os.path.exists(db_path + db_name):
        os.mknod(db_path + db_name)

    # Application configuration

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + db_path + db_name

    db.init_app(app)

    # Defining secret key for encryption and time of expiration of each access token that will be generated
    app.config['JWT_SECRET_KEY'] = str(os.getenv('JWT_SECRET_KEY'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = str(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    jwt.init_app(app)

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', activate_primary_keys)

    api.add_resource(resources.SensorResource, '/sensor/<id_num>')
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.UnverifiedSeismResource, '/unverified-seism/<id_num>')
    api.add_resource(resources.UnverifiedSeismsResource, '/unverified-seisms')
    api.add_resource(resources.VerifiedSeismResource, '/verified-seism/<id_num>')
    api.add_resource(resources.VerifiedSeismsResource, '/verified-seisms')
    api.add_resource(resources.UserResource, '/user/<id_num>')
    api.add_resource(resources.UsersResource, '/users')

    app.register_blueprint(resources.auth)

    api.init_app(app)

    return app
