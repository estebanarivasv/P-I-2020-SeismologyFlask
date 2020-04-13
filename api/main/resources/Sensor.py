from flask_restful import Resource
from flask import request, jsonify
from main import db
from main.models import SensorModel


class Sensor(Resource):

    def get(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        return sensor.to_json()

    def delete(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        db.session.delete(sensor)
        db.session.commit()
        return 'Sensor removed successfully', 204

    def put(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            setattr(sensor, key, value)
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201


class Sensors(Resource):

    def get(self):
        sensors = db.session.query(SensorModel).all()
        return jsonify({'sensors': [sensor.to_json() for sensor in sensors]})

    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201
