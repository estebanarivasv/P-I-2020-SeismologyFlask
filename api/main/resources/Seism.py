from flask_restful import Resource
from flask import request, jsonify
from main.models import SeismModule
from main import db


import time
from random import random, randint, uniform


def create_random():
    value_sensor = {
        'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
        'depth': randint(5, 250),
        'magnitude': round(uniform(2.0, 5.5), 1),
        'latitude': uniform(-180, 180),
        'longitude': uniform(-90, 90),
        'verified': bool(random.getrandbits(1))

    }
    return value_sensor


class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModule).get_or_404(id_num, verified=True)
        return verified_seism.to_json()


class VerifiedSeisms(Resource):

    def get(self):
        verified_seisms = db.session.query(SeismModule).all(verified=True)
        return jsonify({'verified_seisms': [verified_seism.to_json() for verified_seism in verified_seisms]})


class UnverifiedSeism(Resource):

    def get(self, id_num):
        unverified_seism = db.session.query(SeismModule).get_or_404(id_num, verified=False)
        return unverified_seism.to_json()

    def delete(self, id_num):
        unverified_seism = db.session.query(SeismModule).get_or_404(id_num, verified=False)
        db.session.delete(unverified_seism)
        db.session.commit()
        return '', 204

    def put(self, id_num):
        unverified_seism = db.session.query(SeismModule).get_or_404(id_num, verified=False)
        data = request.get_json().items()
        for key, value in data:
            setattr(unverified_seism, key, value)
        db.session.add(unverified_seism)
        db.session.commit()
        return unverified_seism.to_json(), 201


class UnverifiedSeisms(Resource):

    def get(self):
        unverified_seisms = db.session.query(SeismModule).all()
        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})

    def post(self):
        sensor = SeismModule.from_json(create_random())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201
