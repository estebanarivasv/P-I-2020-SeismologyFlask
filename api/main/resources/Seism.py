from flask_restful import Resource
from flask import request

SEISMS = {
    1: {'ref_number': '001', 'date': '11-02-2019', 'time': '20:59', 'magnitude': '5.16'},
    2: {'ref_number': '005', 'date': '25-05-2019', 'time': '13:40', 'magnitude': '9.75'},
    3: {'ref_number': '013', 'date': '19-08-2019', 'time': '16:36', 'magnitude': '4.63'},
    4: {'ref_number': '019', 'date': '04-11-2019', 'time': '18:42', 'magnitude': '11.24'},
    5: {'ref_number': '020', 'date': '16-12-2019', 'time': '07:12', 'magnitude': '6.78'},
    6: {'ref_number': '049', 'date': '02-02-2020', 'time': '23:20', 'magnitude': '15.08'}
}


class VerifiedSeism(Resource):

    def get(self, id_num):
        if int(id_num) in SEISMS:
            return SEISMS[int(id_num)], 200
        return '', 404


class VerifiedSeisms(Resource):

    def get(self):
        return SEISMS, 200


class UnverifiedSeism(Resource):

    def get(self, id_num):
        if int(id_num) in SEISMS:
            return SEISMS[int(id_num)], 200
        return '', 404

    def put(self, id_num):
        if int(id_num) in SEISMS:
            seism = SEISMS[int(id_num)]
            data = request.get_json()
            seism.update(data)
            return seism, 201
        return 404

    def delete(self, id_num):
        if int(id_num) in SEISMS:
            del SEISMS[int(id_num)]
            return '', 204
        return '', 404


class UnverifiedSeisms(Resource):

    def get(self):
        return SEISMS, 200
