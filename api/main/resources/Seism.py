from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from random import randint, uniform

from main import db
from main.models import SeismModel
from main.models.Sensor import Sensor as SensorModel
from main.authentication import admin_login_required

from datetime import datetime


class VerifiedSeism(Resource):

    def get(self, id_num):
        verified_seism = db.session.query(SeismModel).get_or_404(id_num)
        return verified_seism.to_json_public()

    @admin_login_required
    def put(self, id_num):
        verified_seism = db.session.query(SeismModel).get_or_404(id_num)
        data = request.get_json().items()
        for key, value in data:
            if key == 'datetime':
                setattr(verified_seism, key, datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
            elif key == 'sensor_id':
                setattr(verified_seism, key, value)
            else:
                setattr(verified_seism, key, value)
        db.session.add(verified_seism)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return '', 409
        return verified_seism.to_json(), 201


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
            if key == "from_date":
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                verified_seisms = verified_seisms.filter(SeismModel.datetime >= value)
            if key == "to_date":
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                verified_seisms = verified_seisms.filter(SeismModel.datetime <= value)
            if key == "mag_min":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude >= value)
            if key == "mag_max":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude <= value)
            if key == "depth_min":
                verified_seisms = verified_seisms.filter(SeismModel.depth >= value)
            if key == "depth_max":
                verified_seisms = verified_seisms.filter(SeismModel.depth <= value)
            if key == "sensor_name":
                verified_seisms = verified_seisms.join(SeismModel.sensor).filter(
                    SensorModel.name.like("%" + str(value) + "%"))

            # Sorting: datetime (descendant, ascendant), sensor.name (descendant, ascendant)
            if key == "sort_by":
                if value == "datetime[desc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime[asc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.datetime.asc())
                if value == "sensor_name[desc]":
                    verified_seisms = verified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor_name[asc]":
                    verified_seisms = verified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())
                if value == "magnitude[desc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude[asc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.magnitude.asc())
                if value == "depth[desc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.depth.desc())
                if value == "depth[asc]":
                    verified_seisms = verified_seisms.order_by(SeismModel.depth.asc())

        # Paginates the filtered result and returns a Paginate object
        verified_seisms = verified_seisms.paginate(page_num, elem_per_page, raise_error, max_elem_per_page)


        return jsonify({
                'verified_seisms': [verified_seism.to_json_public() for verified_seism in verified_seisms.items],
                'page_num': page_num,
                'elem_per_page': elem_per_page,
                'total_pages': verified_seisms.pages,
                'items_num': len(verified_seisms.items)
                })


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

        # We obtain the user's identity and the JWT claims. We filter the seisms for assigned for the logged user
        
        user_id = int(get_jwt_identity())
        claims = get_jwt_claims()

        page_num = 1
        elem_per_page = 10
        raise_error = True
        max_elem_per_page = 50

        # Obtains items from json
        filters = request.get_json().items()

        # Filters in unverified_seisms
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        if not claims['admin']:
            # Filters the left associated seisms with the seismologist
            unverified_seisms = unverified_seisms.join(SeismModel.sensor).filter(SensorModel.user_id == user_id)
        

        for key, value in filters:

            # Page settings from json
            if key == "page_num":
                page_num = int(value)
            if key == "elem_per_page":
                elem_per_page = int(value)

            # Filters: sensor_id
            if key == "sensor_id":
                unverified_seisms = unverified_seisms.join(SeismModel.sensor).filter(SensorModel.id_num == value)
            if key == "from_date":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime >= value)
            if key == "to_date":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime <= value)

            # Sorting: datetime (descendant, ascendant)
            if key == "sort_by":

                # Sort by datetime
                if value == "sensor_name[desc]":
                    unverified_seisms = unverified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor_name[asc]":
                    unverified_seisms = unverified_seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())
                if value == "datetime[desc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime[asc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.datetime.asc())
                if value == "magnitude[desc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude[asc]":
                    unverified_seisms = unverified_seisms.order_by(SeismModel.magnitude.asc())


        unverified_seisms = unverified_seisms.paginate(page_num, elem_per_page, raise_error, max_elem_per_page)

        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms.items],
                        'page_num': page_num,
                        'elem_per_page': elem_per_page,
                        'total_pages': unverified_seisms.pages,
                        'items_num': unverified_seisms.total
                        })