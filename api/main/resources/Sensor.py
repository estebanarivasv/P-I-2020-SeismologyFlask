from flask_restful import Resource
from flask import request, jsonify
from main import db
from main.models import SensorModule


class Sensor(Resource):

    def get(self, id_num):
        sensor = db.session.query(SensorModule).get_or_404(id_num)
        return sensor.to_json()

    def delete(self, id_num):
        sensor = db.session.query(SensorModule).get_or_404(id_num)
        db.session.delete(sensor)
        db.session.commit()
        return '', 204

    def put(self, id_num):
        sensor = db.session.query(SensorModule).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            setattr(sensor, key, value)
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201


class Sensors(Resource):

    def get(self):
        sensors = db.session.query(SensorModule).all()
        return jsonify({'sensors': [sensor.to_json() for sensor in sensors]})

    def post(self):
        sensor = SensorModule.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201
