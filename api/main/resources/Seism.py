from flask_restful import Resource
from flask import request, jsonify
from main import db
from main.models import SeismModel
from datetime import datetime


class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModel).get_or_404(id_num)
        print(verified_seism)
        return verified_seism.to_json()


class VerifiedSeisms(Resource):

    def get(self):
        filters = request.get_json().items()
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True).all()
        for key, value in filters:
            if key is "id_num":
                verified_seisms = verified_seisms.filter(SeismModel.id_num == value)
            elif key is "datetime":
                verified_seisms = verified_seisms.filter(SeismModel.datetime == value)
            elif key is "magnitude":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude == value)
            elif key is "sensor_id":
                verified_seisms = verified_seisms.filter(SeismModel.sensor_id == value)
            verified_seisms.all()
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
        return 'Unverified-seism removed successfully', 204

    def put(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            if key == 'datetime':
                setattr(unverified_seism, key, datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
            else:
                setattr(unverified_seism, key, value)
        db.session.add(unverified_seism)
        db.session.commit()
        return unverified_seism.to_json(), 201


class UnverifiedSeisms(Resource):

    def get(self):

        filters = request.get_json().items()
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False).all()

        # filters by id_num, datetime, magnitude, sensor_id
        for key, value in filters:
            if key is "id_num":
                unverified_seisms = unverified_seisms.filter(SeismModel.id_num == value)
            elif key is "datetime":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime == value)
            elif key is "magnitude":
                unverified_seisms = unverified_seisms.filter(SeismModel.magnitude == value)
            elif key is "sensor_id":
                unverified_seisms = unverified_seisms.filter(SeismModel.sensor_id == value)
            unverified_seisms.all()

        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})
