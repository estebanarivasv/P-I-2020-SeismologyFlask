from flask_restful import Resource
from flask import request, jsonify
from main import db
from main.models import SeismModel



class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModel).filter(SeismModel.verified == True).get_or_404(id_num)
        return verified_seism.to_json()


class VerifiedSeisms(Resource):

    def get(self):
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True).all()
        return jsonify({'verified_seisms': [verified_seism.to_json() for verified_seism in verified_seisms]})


class UnverifiedSeism(Resource):

    def get(self, id_num):
        unverified_seism = db.session.query(SeismModel).filter(SeismModel.verified == False).get_or_404(id_num)
        return unverified_seism.to_json()

    def delete(self, id_num):
        unverified_seism = db.session.query(SeismModel).filter(SeismModel.verified == False).get_or_404(id_num)
        db.session.delete(unverified_seism)
        db.session.commit()
        return '', 204

    def put(self, id_num):
        unverified_seism = db.session.query(SeismModel).filter(SeismModel.verified == False).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            setattr(unverified_seism, key, value)
        db.session.add(unverified_seism)
        db.session.commit()
        return unverified_seism.to_json(), 201


class UnverifiedSeisms(Resource):

    def get(self):
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False).all()
        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})
