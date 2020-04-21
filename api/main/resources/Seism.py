from flask_restful import Resource
from flask import request, jsonify

from main import db
from main.models import SeismModel
from main.models.Sensor import Sensor as SensorModel

from datetime import datetime


class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModel).get_or_404(id_num)
        print(verified_seism)
        return verified_seism.to_json()


class VerifiedSeisms(Resource):

    def get(self):
        filters = request.get_json().items()
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        print(filters)
        for (key, value) in filters:
            if key == "id_num":
                verified_seisms = verified_seisms.filter(SeismModel.id_num == value)
            if key == "datetime":
                verified_seisms = verified_seisms.filter(SeismModel.datetime == value)
            if key == "magnitude":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude == value)
            if key == "sensor_id":
                verified_seisms = verified_seisms.filter(SeismModel.sensor_id == value)
            verified_seisms.all()
        print(verified_seisms)
        return jsonify({'verified_seisms': [verified_seism.to_json() for verified_seism in verified_seisms]})


class UnverifiedSeism(Resource):

    def get(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        return unverified_seism.to_json()

    def delete(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        db.session.delete(unverified_seism)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return '', 204

    def put(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            if key == 'datetime':
                setattr(unverified_seism, key, datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
            elif key == 'sensor_id':
                i = db.session.query(SensorModel).get_or_404(value)
                setattr(unverified_seism, key, value)
            else:
                setattr(unverified_seism, key, value)
        db.session.add(unverified_seism)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return unverified_seism.to_json(), 201


class UnverifiedSeisms(Resource):

    def get(self):
        filters = request.get_json().items()
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        # filters by id_num, datetime, magnitude, sensor_id
        for key, value in filters:
            if key == "id_num":
                unverified_seisms = unverified_seisms.filter(SeismModel.id_num == value)
            elif key == "datetime":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime == value)
            elif key == "magnitude":
                unverified_seisms = unverified_seisms.filter(SeismModel.magnitude == value)
            elif key == "sensor_id":
                unverified_seisms = unverified_seisms.filter(SeismModel.sensor_id == value)
            unverified_seisms.all()

        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})
