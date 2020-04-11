import main.models.Seism as SeismModule
import main.models.Sensor as SensorModule
import main.models.User as UserModule
from main import db

from app import app

from random import randint, uniform, getrandbits
from datetime import datetime

"""THIS SCRIPT WAS OBTAINED FROM
https://stackoverflow.com/questions/21014618/python-randomly-generated-ip-address-as-string"""


def create_random_ip():
    ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
    return ip


"""END OF COPIED SCRIPT"""


def create_random_email():
    name = input("User name: ")
    surname = input("User surname: ")
    email = (name+"."+surname).lower() + "@seismologyinstitute.com"
    return email


def create_user_permissions():
    opt = input("Admin? (Y-N): ")
    while True:
        if opt == "Y" or opt == "y":
            return True
        elif opt == "N" or opt == "n":
            return False
        else:
            print("Try again.")


def add_random_seism_to_db():
    with app.app_context():
        random_seism = SeismModule.Seism(
            id_num=randint(0, 250),
            datetime=datetime(
                randint(2000, 2020),
                randint(1, 12),
                randint(1, 28),
                randint(00, 23),
                randint(0, 60),
                randint(0, 60)
            ),
            depth=randint(5, 250),
            magnitude=round(uniform(2.0, 5.5), 1),
            latitude=uniform(-180, 180),
            longitude=uniform(-90, 90),
            verified=bool(getrandbits(1))
        )
        """sensor_id="""

        db.session.add(random_seism)
        db.session.commit()


def add_random_sensor_to_db():
    with app.app_context():
        random_sensor = SensorModule.Sensor(
            id_num=randint(0, 250),
            name=input("Sensor name: "),
            ip=create_random_ip(),
            port=randint(1, 65535),
            status=bool(getrandbits(1)),
            active=bool(getrandbits(1))
        )
        db.session.add(random_sensor)
        db.session.commit()


def add_random_user_to_db():
    with app.app_context():
        random_user = UserModule.User(
            id_num=randint(0, 250),
            email=create_random_email(),
            password=input("Password: "),
            admin=create_user_permissions()
        )
        db.session.add(random_user)
        db.session.commit()


add_random_seism_to_db()
add_random_sensor_to_db()
add_random_user_to_db()
