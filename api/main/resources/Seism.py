from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from main import db
from main.models import SeismModel
from main.models.Sensor import Sensor as SensorModel

from datetime import datetime


class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModel).get_or_404(id_num)
        return verified_seism.to_json_public()


class VerifiedSeisms(Resource):

    # Define filters, sorting, pagination

    def get(self):

        page_num = 1
        elem_per_page = 25
        raise_error = True
        max_elem_per_page = 10000

        # Obtains items from json
        filters = request.get_json().items()

        # Filters in verified seisms
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)

        for (key, value) in filters:

            # Page settings from json
            if key == "page_num":
                page_num = int(value)
            if key == "elem_per_page":
                elem_per_page = int(value)

            # Filters: datetime, magnitude, sensor.name
            if key == "datetime":
                verified_seisms = verified_seisms.filter(SeismModel.datetime.like("%"+str(value)+"%"))
            if key == "magnitude":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude.like("%"+str(value)+"%"))
            if key == "sensor.name":
                verified_seisms = verified_seisms.join(SeismModel.sensor).filter(SensorModel.name.like("%"+str(value)+"%"))

            # Sorting: datetime (descendant, ascendant), sensor.name (descendant, ascendant)
            if key == "sort_by":
                if value == "datetime[desc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime[asc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.datetime.asc())
                if value == "sensor.name[desc]":
                    verified_seisms = verified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor.name[asc]":
                    verified_seisms = verified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())

        # Paginates the filtered result and returns a Paginate object
        verified_seisms = verified_seisms.paginate(page_num, elem_per_page, raise_error, max_elem_per_page)

        return jsonify({'verified_seisms': [verified_seism.to_json_public() for verified_seism in verified_seisms.items]})


class UnverifiedSeism(Resource):

    @jwt_required
    def get(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        return unverified_seism.to_json()

    @jwt_required
    def delete(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        db.session.delete(unverified_seism)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return '', 204

    @jwt_required
    def put(self, id_num):
        unverified_seism = db.session.query(SeismModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            if key == 'datetime':
                setattr(unverified_seism, key, datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
            elif key == 'sensor_id':
                i = db.session.query(SensorModel).get(value)
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

    @jwt_required
    def get(self):

        page_num = 1
        elem_per_page = 10
        raise_error = True
        max_elem_per_page = 50

        # Obtains items from json
        filters = request.get_json().items()

        # Filters in unverified_seisms
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        for key, value in filters:

            # Page settings from json
            if key == "page_num":
                page_num = int(value)
            if key == "elem_per_page":
                elem_per_page = int(value)

            # Filters: sensor_id
            if key == "sensor_id":
                unverified_seisms = unverified_seisms.filter(SeismModel.sensor_id.like("%"+str(value)+"%"))

            # Sorting: datetime (descendant, ascendant)
            if key == "sort_by":

                # Sort by datetime
                if value == "datetime[desc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime[asc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.datetime.asc())

        unverified_seisms = unverified_seisms.paginate(page_num, elem_per_page, raise_error, max_elem_per_page)

        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in
                                              unverified_seisms.items]})
