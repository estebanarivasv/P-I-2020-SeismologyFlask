import json
import socket
import sys
import time
from random import randint, uniform
from datetime import datetime

def send_data():
    value_sensor = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'depth': randint(5, 250),
        'magnitude': round(uniform(2.0, 5.5), 1),
        'latitude': uniform(-180, 180),
        'longitude': uniform(-90, 90)
    }
    return value_sensor


if __name__ == '__main__':

    # We create the sensor's server socket
    sensor_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if len(sys.argv[1:]) < 1:
        print("Usage:\npython3 sensor_socket <port>")
    else:
        # Default ip 127.0.0.1
        host = ""
        port = int(sys.argv[1])

        sensor_serv.bind((host, port))

        while True:
            print(f"Listening in {host}, {port}.")
            data, connection = sensor_serv.recvfrom(1024)

            address = connection[0]
            port = connection[1]

            print(f"Data request from {address}, {port}")

            msg = json.dumps(send_data())
            sensor_serv.sendto(msg.encode(), connection)
