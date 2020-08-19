from flask_restful import Resource
from flask import request, jsonify

from main import db
from main.models import UserModel
from main.authentication import admin_login_required


class User(Resource):

    #@admin_login_required
    def get(self, id_num):
        user = db.session.query(UserModel).get_or_404(id_num)
        return user.to_json()

    #@admin_login_required
    def delete(self, id_num):
        user = db.session.query(UserModel).get_or_404(id_num)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return 'User deleted', 204

    #@admin_login_required
    def put(self, id_num):
        user = db.session.query(UserModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, values in data:
            setattr(user, key, values)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201


class Users(Resource):

    #@admin_login_required
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'users': [user.to_json() for user in users]})

    #@admin_login_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        email_exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
        if email_exists:
            return 'The entered email address has already been registered', 409
        else:            
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201
