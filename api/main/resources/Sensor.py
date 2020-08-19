from flask_restful import Resource
from flask import request, jsonify

from main import db
from main.models import SensorModel
from main.models.User import User as UserModel
from main.authentication import admin_login_required


class Sensor(Resource):

    #@admin_login_required
    def get(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        return sensor.to_json()

    #@admin_login_required
    def delete(self, id_num):
        sensor = db.session.query(SensorModel).get_or_404(id_num)
        db.session.delete(sensor)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return '', 204

    #@admin_login_required
    def put(self, id_num):
        sensor = db.session.query(SensorModel).get(id_num)
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

    #@admin_login_required
    def get(self):

        page_num = 1
        elem_per_page = 25
        raise_error = True
        max_elem_per_page = 50

        filters = request.get_json().items()
        sensors = db.session.query(SensorModel)

        for key, value in filters:

            # Page settings from json

            if key == "page_num":
                page_num = int(value)
            if key == "elem_per_page":
                elem_per_page = int(value)

            # Filters: user_id (null/not-null), active, status (sending / not-sending data), user.email

            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "user_id":
                sensors = sensors.filter(SensorModel.user_id.like(value))
            if key == "user.email":
                sensors = sensors.join(SensorModel.user).filter(UserModel.email.like("%" + value + "%"))

            # Sorting: name (ascendant, descendant), user_id (ascendant, descendant), active (ascendant, descendant)
            #          status (ascendant, descendant), user.email (ascendant, descendant)

            if key == "sort_by":
                if value == "name[desc]":
                    sensors = sensors.order_by(SensorModel.name.desc())
                if value == "name[asc]":
                    sensors = sensors.order_by(SensorModel.name.asc())
                if value == "user_id[desc]":
                    sensors = sensors.order_by(SensorModel.user_id.desc())
                if value == "user_id[asc]":
                    sensors = sensors.order_by(SensorModel.user_id.asc())
                if value == "active[desc]":
                    sensors = sensors.order_by(SensorModel.active.desc())
                if value == "active[asc]":
                    sensors = sensors.order_by(SensorModel.active.asc())
                if value == "status[desc]":
                    sensors = sensors.order_by(SensorModel.status.desc())
                if value == "status[asc]":
                    sensors = sensors.order_by(SensorModel.status.asc())
                if value == "user.email[desc]":
                    sensors = sensors.join(SensorModel.user).order_by(UserModel.email.desc())
                if value == "user.email[asc]":
                    sensors = sensors.join(SensorModel.user).order_by(UserModel.email.asc())

        sensors = sensors.paginate(page_num, elem_per_page, raise_error, max_elem_per_page)
        return jsonify({'sensors': [sensor.to_json() for sensor in sensors.items]})

    #@admin_login_required
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201
