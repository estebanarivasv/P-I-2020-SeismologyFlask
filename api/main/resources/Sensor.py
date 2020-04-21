from flask_restful import Resource
from flask import request, jsonify

from main import db
from main.models import SensorModel
from main.models.User import User as UserModel


class Sensor(Resource):

    def get(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        return sensor.to_json()

    def delete(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        db.session.delete(sensor)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return '', 204

    def put(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        filters = request.get_json().items()
        for key, value in filters:
            if key == 'user_id':
                i = db.session.query(UserModel).get_or_404(value)
                setattr(sensor, key, value)
            else:
                setattr(sensor, key, value)

        db.session.add(sensor)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
            # Verifies if the user_id exists in User table. If false, returns exception.
        return sensor.to_json(), 201


class Sensors(Resource):

    def get(self):
        filters = request.get_json().items()
        sensors = db.session.query(SensorModel)

        # filters by id_num, name, ip, port, status, active, user_id
        for key, value in filters:
            if key == "id_num":
                sensors = sensors.filter(SensorModel.id_num == value)
            if key == "name":
                sensors = sensors.filter(SensorModel.name == value)
            if key == "ip":
                sensors = sensors.filter(SensorModel.ip == value)
            if key == "port":
                sensors = sensors.filter(SensorModel.port == value)
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "user_id":
                sensors = sensors.filter(SensorModel.user_id == value)
            sensors.all()

        return jsonify({'sensors': [sensor.to_json() for sensor in sensors]})

    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        for key, value in sensor:
            if key == 'user_id':
                i = db.session.query(UserModel).get_or_404(value)
                setattr(sensor, key, value)
            else:
                setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return sensor.to_json(), 201
