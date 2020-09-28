from main import create_app
from main import db
from main.models import UserModel, SensorModel, SeismModel
from main.utilities import create_socket

from datetime import datetime
import os
import time
import threading
import socket
import json


def create_admins_in_db():
    admins = db.session.query(UserModel.id_num).filter(UserModel.admin == True)
    admins_list = [admin for admin, in admins]
    if len(admins_list) == 0:
        user = UserModel(
            email=os.getenv('ADMIN_MAIL'),
            plain_password=os.getenv('ADMIN_PLAIN_PASSWORD'),
            admin=bool(os.getenv('ADMIN_BOOL'))
        )
        db.session.add(user)
        db.session.commit()
    else:
        pass


def call_sensors():
    time.sleep(5)
    with app.app_context():
        sensors = db.session.query(SensorModel).filter(SensorModel.status == True, SensorModel.active == True).all()
        if len(sensors) == 0:
            print("\n--------------------------------------------------------\n"
                  "There are not available sensors.\nPlease run sensors checking in order to get them working."
                  "\n--------------------------------------------------------\n")
        else:
            client = create_socket()
            while client:
                for sensor in sensors:
                    client.sendto(b"", (sensor.ip, sensor.port))
                    try:
                        data, _addr = client.recvfrom(1024)
                        seism = json.loads(data.decode())
                        print("  ", sensor, "\t", seism)
                        u_seism = SeismModel(
                            datetime=datetime.strptime(seism.get('datetime'), '%Y-%m-%d %H:%M:%S'),
                            depth=int(seism['depth']),
                            magnitude=float(seism['magnitude']),
                            latitude=seism['latitude'],
                            longitude=seism['longitude'],
                            verified=False,
                            sensor_id=int(sensor.id_num)
                        )
                        db.session.add(u_seism)
                        try:
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print(e)

                    except socket.timeout:
                        sensor.status = False
                        db.session.add(sensor)
                        db.session.commit()
                        print(f"Sensor {sensor.name} not responding.")
                time.sleep(300)


# Creating Flask app instance
app = create_app()

# Loading app context
app.app_context().push()

# If this script is run, the db is created; and the app is run in an specific port
if __name__ == '__main__':
    db.create_all()
    threading.Thread(target=call_sensors).start()
    create_admins_in_db()
    app.run(debug=False, port=os.getenv('PORT'))  # Set to false because it was creating multiple threads
