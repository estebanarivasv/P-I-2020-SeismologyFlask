import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

# Flask API RESTFUL principal inizilization
api = Api()

# Database principal inizilization
db = SQLAlchemy()

# Authentication handler principal inizilization
jwt = JWTManager()

# Outgoing server sender principal inizilization
out_server_sender = Mail()

# Importing blueprints and resources
import main.resources as resources
from main.authentication import auth_blueprint
from main.mail import stopped_sensors_blueprint


# Function that, when executed, activates primary keys recognition in the SQLite DB
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
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    jwt.init_app(app)

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    out_server_sender.init_app(app)

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

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(stopped_sensors_blueprint)

    api.init_app(app)

    return app
