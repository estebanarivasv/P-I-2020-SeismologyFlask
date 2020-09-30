import csv
import datetime
import io
import json
from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash, make_response

import main.forms as f
from main.utilities.api_querying import makeRequest

"""
-----------------------------------------------------------------------------
                        V E R I F I E D   S E I S M S
-----------------------------------------------------------------------------
"""

v_seism = Blueprint('v_seism', __name__, url_prefix='/verified-seisms/')


@v_seism.route('/')
def main():
    url = current_app.config["API_URL"] + "/verified-seisms"

    filters = f.VSeismsFilterForm(request.args, meta={'csrf': False})

    query = makeRequest("GET", url)
    verified_seisms = json.loads(query.text)["verified_seisms"]

    data = {}

    file_name = "total_vseisms"

    if filters.validate():
        if filters.depth_min.data is not None:
            data["depth_min"] = filters.depth_min.data
            file_name = file_name + "-" + str(filters.depth_min.data)
        if filters.depth_max.data is not None:
            data["depth_max"] = filters.depth_max.data
            file_name = file_name + "-" + str(filters.depth_max.data)
        if filters.mag_min.data is not None:
            data["mag_min"] = filters.mag_min.data
            file_name = file_name + "-" + str(filters.mag_min.data)
        if filters.mag_max.data is not None:
            data["mag_max"] = filters.mag_max.data
            file_name = file_name + "-" + str(filters.mag_max.data)
        if filters.sensor_name.data is not None and filters.sensor_name.data != "":
            data["sensor_name"] = filters.sensor_name.data
            file_name = file_name + "-" + str(filters.sensor_name.data)

    if "from_datetime" in request.args and request.args["from_datetime"] != "":
        date = datetime.datetime.strptime(request.args.get("from_datetime", ""), "%Y-%m-%dT%H:%M")
        data["from_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        file_name = file_name + "-" + str(datetime.datetime.strftime(date, "%Y%m%dT%H%M%S"))

    if "to_datetime" in request.args and request.args["to_datetime"] != "":
        date = datetime.datetime.strptime(request.args.get("to_datetime", ""), "%Y-%m-%dT%H:%M")
        data["to_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        file_name = file_name + "-" + str(datetime.datetime.strftime(date, "%Y%m%dT%H%M%S"))

    if 'page_num' in request.args:
        data["page_num"] = request.args.get('page_num', '')

    if 'sort_by' in request.args and request.args['sort_by'] != "":
        data["sort_by"] = request.args.get('sort_by', '')
        filters.sort_by.data = data["sort_by"]

    if 'elem_per_page' in request.args and request.args['elem_per_page'] != "":
        data["elem_per_page"] = request.args.get('elem_per_page', '')

    if 'download' in request.args:
        if request.args.get('download', '') == 'Download seisms into CSV':
            # Start parameters
            code = 200
            page_num = 1
            seisms_list = []

            while code == 200:
                data['page_num'] = page_num

                print(json.dumps(data))
                query = makeRequest("GET", url, data=json.dumps(data))
                code = query.status_code

                if query.status_code == 200:
                    v_seisms = json.loads(query.text)["verified_seisms"]

                    for seism in v_seisms:
                        seism_dict = {
                            'datetime': seism["datetime"],
                            'depth': seism["depth"],
                            'magnitude': seism["magnitude"],
                            'latitude': seism["latitude"],
                            'longitude': seism["longitude"],
                            'sensor': seism["sensor"]["name"]
                        }
                        seisms_list.append(seism_dict)
                    page_num += 1

            if seisms_list:
                # Str IO and CSV writer inicialization. Dictionary's keys are parsed as headers
                si = io.StringIO()
                fc = csv.DictWriter(si, fieldnames=seisms_list[0].keys(), )

                # CSV writing. First titles, then rows
                fc.writeheader()
                fc.writerows(seisms_list)

                output = make_response(si.getvalue())

                # Headers for file download
                output.headers["Content-Disposition"] = "attachment; filename=" + file_name + ".csv"
                output.headers["Content-type"] = "text/csv"

                return output

    data = json.dumps(data)
    query = makeRequest("GET", url, data=data)

    if query.status_code == 200:
        verified_seisms = json.loads(query.text)["verified_seisms"]

        pagination = {"items_num": json.loads(query.text)["items_num"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page_num": json.loads(query.text)["page_num"]}

        return render_template('/derived/verified-seisms/main.html',
                               verified_seisms=verified_seisms,
                               filters=filters,
                               pagination=pagination)

    else:
        return redirect(url_for('v_seism.main'))


@v_seism.route('/view/<int:id>')
def view_vseism(id):
    url = current_app.config["API_URL"] + "/verified-seism/" + str(id)
    query = makeRequest("GET", url)
    if query.status_code == 404:
        flash("Seism not found", "warning")
        return redirect(url_for('v_seism.main'))
    verified_seism = json.loads(query.text)
    return render_template('/derived/verified-seisms/view-vseism.html', verified_seism=verified_seism)
