from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModule


class User(Resource):
    def get(self, id_num):
        user = db.session.query(UserModule).get_or_404(id_num)
        return user.to_json()

    def delete(self, id_num):
        user = db.session.query(UserModule).get_or_404(id_num)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    def put(self, id_num):
        user = db.session.query(UserModule).get_or_404(id_num)
        data = request.get_json().items()
        for key, values in data:
            setattr(user, key, values)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

class Users(Resource):
    def get(self):
        users = db.session.query(UserModule).all()
        return jsonify({'users': [user.to_json() for user in users]})

    def post(self):
        user = UserModule.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

