import random
import string
from random import randint, getrandbits

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


def add_random_sensor_to_db(id_number):
    with app.app_context():
        random_sensor = SensorModule.Sensor(
            name=random_generator(),
            ip=create_random_ip(),
            port=randint(1, 65535),
            status=bool(getrandbits(1)),
            active=bool(getrandbits(1)),
            user_id=randint(6, 15)
        )
        db.session.add(random_sensor)
        db.session.commit()


for i in range(30):
    add_random_sensor_to_db(i)
