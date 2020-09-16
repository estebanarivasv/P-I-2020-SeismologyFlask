from main import create_app
app = create_app()
app.app_context().push()
import os, socket, threading, time


sensors = [
    {'name':'SensorA','IP':'127.0.0.1','PORT': 5500, 'status':1, 'active':1},
    {'name':'SensorB','IP':'127.0.0.1','PORT': 5501, 'status':1, 'active':1},
    {'name':'SensorC','IP':'127.0.0.1','PORT': 5502, 'status':1, 'active':1}
]

#Crear socket
def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        return s
    except socket.error:
        print('Failed to create socket')
        return None

#Checkear estado sensor
def check_sensor(id):
    sensor = sensors[id]
    s = create_socket()
    if s:
        s.sendto(b" ", (sensor["IP"], sensor["PORT"]))
        try :
            d = s.recvfrom(1024)[0]
            sensors[id]["status"] = 1
        except socket.timeout:
            print("Sensor"+sensor["name"]+" no responde")

#Llamar a sensores
def call_sensors():
    s = create_socket()
    while s:
        for sensor in sensors:
            if sensor['active'] and sensor['status']:
                s.sendto(b" ", (sensor["IP"], sensor["PORT"]))
                try :
                    d = s.recvfrom(1024)[0]
                    print(d)
                except socket.timeout:
                    sensor["status"] = 0
                    print("Sensor "+sensor["name"]+" no responde")
        time.sleep(2)

@app.route('/<int:id>')
def index(id):
    check_sensor(id)
    return "Check"

if __name__ == '__main__':
    print("Función principal")
    threading.Thread(target=call_sensors).start()
    app.run(debug = False, port = os.getenv("PORT"))
