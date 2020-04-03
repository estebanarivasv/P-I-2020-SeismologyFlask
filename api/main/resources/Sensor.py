from flask_restful import Resource
from flask import request

SENSORS = {
    1: {'ref_number': '0000', 'name': 'Tokyo, Japan', 'status': 'enabled'},
    2: {'ref_number': '0010', 'name': 'Chicago, USA', 'status': 'disabled'},
    3: {'ref_number': '0250', 'name': 'Hefei, China', 'status': 'enabled'},
    4: {'ref_number': '0015', 'name': 'Cape Town, South Africa', 'status': 'disabled'},
    5: {'ref_number': '0165', 'name': 'Montevideo, Uruguay', 'status': 'enabled'},
    6: {'ref_number': '0213', 'name': 'Milan, Italy', 'status': 'disabled'}
}


class Sensor(Resource):

    def get(self, id_num):
        if int(id_num) in SENSORS:
            return SENSORS[int(id_num)], 200
        return '', 404

    def put(self, id_num):
        if int(id_num) in SENSORS:
            sensor = SENSORS[int(id_num)]
            data = request.get_json()
            sensor.update(data)
            return sensor, 201
        return '', 404

    def delete(self, id_num):
        if int(id_num) in SENSORS:
            del SENSORS[int(id_num)]
            return '', 204
        return '', 404


class Sensors(Resource):

    def get(self):
        return SENSORS, 200

    def post(self):
        sensor = request.get_json()
        print(SENSORS.keys())
        print(max(SENSORS.keys()))
        id_num = max(SENSORS.keys()) + 1
        SENSORS[id_num] = sensor
        return SENSORS[id_num], 201
