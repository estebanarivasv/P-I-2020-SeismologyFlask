import random
import string
from datetime import datetime
from random import randint, uniform, getrandbits

import main.models.Seism as SeismModule
import main.models.Sensor as SensorModule
import main.models.User as UserModule

from app import app
from main import db


def create_random_ip():
    ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
    return ip


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def create_random_email():
    name = input("User name: ")
    surname = input("User surname: ")
    email = (name + "." + surname).lower() + "@seismologyinstitute.com"
    return email


def create_user_permissions():
    opt = input("Admin? (Y-N): ")
    i = 0
    while i == 0:
        if opt == "Y" or opt == "y":
            i = 1
            return True
        elif opt == "N" or opt == "n":
            i = 1
            return False
        else:
            print("Try again.")


def add_random_seism_to_db():
    with app.app_context():
        random_seism = SeismModule.Seism(
            id_num=randint(0, 10000000),
            datetime=datetime(
                randint(2000, 2020),
                randint(1, 12),
                randint(1, 28),
                randint(00, 23),
                randint(0, 59),
                randint(0, 59)
            ),
            depth=randint(5, 250),
            magnitude=round(uniform(2.0, 5.5), 1),
            latitude=uniform(-180, 180),
            longitude=uniform(-90, 90),
            verified=bool(getrandbits(1)),
            sensor_id=int(input("Sensor id associated with the seism: "))
        )

        db.session.add(random_seism)
        db.session.commit()


def add_random_sensor_to_db(id_number):
    with app.app_context():
        random_sensor = SensorModule.Sensor(
            id_num=id_number,
            name=random_generator(),
            ip=create_random_ip(),
            port=randint(1, 65535),
            status=bool(getrandbits(1)),
            active=bool(getrandbits(1)),
            user_id=int(input("User id associated with the sensor: "))
        )
        db.session.add(random_sensor)
        db.session.commit()


def add_random_user_to_db(id_number):
    with app.app_context():
        random_user = UserModule.User(
            id_num=id_number,
            email=create_random_email(),
            password=input("Password: "),
            admin=create_user_permissions()
        )
        db.session.add(random_user)
        db.session.commit()


for i in range(17):
    add_random_user_to_db(i)
for i in range(30):
    add_random_sensor_to_db(i)
for i in range(60):
    add_random_seism_to_db()
