"""
-----------------------------------------------------------------------------
                    U N V E R I F I E D   S E I S M S
-----------------------------------------------------------------------------
"""

import json

from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from flask_login import login_required

import main.forms as f
from main.utilities.api_querying import makeRequest

u_seism = Blueprint('u_seism', __name__, url_prefix='/unverified-seisms/')


@u_seism.route('/')
@login_required
def main():
    url = current_app.config["API_URL"] + "/unverified-seisms"
    sensors_url = current_app.config["API_URL"] + "/sensors"

    filters = f.USeismsFilterForm(request.args, meta={'csrf': False})

    query = makeRequest("GET", sensors_url, authenticated_user=True)
    sensors = json.loads(query.text)["sensors"]

    filters.sensor_id.choices = [(int(sensor['id_num']), sensor['name']) for sensor in sensors]
    filters.sensor_id.choices.insert(0, [0, "-"])

    data = {}

    print(filters.from_datetime.data, filters.to_datetime.data)
    if filters.validate():
        if filters.sensor_id.data is not None and filters.sensor_id.data != 0:
            data["sensor_id"] = filters.sensor_id.data
        if filters.from_datetime.data is not None:
            data["from_date"] = filters.from_datetime.data.strftime('%Y-%m-%d %H:%M:%S')
        if filters.to_datetime.data is not None:
            data["to_date"] = filters.to_datetime.data.strftime('%Y-%m-%d %H:%M:%S')

    if 'page_num' in request.args:
        data["page_num"] = request.args.get('page_num', '')

    if 'sort_by' in request.args:
        data["sort_by"] = request.args.get('sort_by', '')

    data = json.dumps(data)
    query = makeRequest("GET", url, authenticated_user=True, data=data)

    if query.status_code == 200:

        unverified_seisms = json.loads(query.text)["unverified_seisms"]

        pagination = {"items_num": json.loads(query.text)["items_num"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page_num": json.loads(query.text)["page_num"]}

        return render_template('/derived/unverified-seisms/main.html',
                               unverified_seisms=unverified_seisms,
                               filters=filters,
                               pagination=pagination)
    else:
        return redirect(url_for('u_seism.main'))


@u_seism.route('/edit/<int:id>', methods=["POST", "GET"])
@login_required
def edit_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    form = f.SeismForm()

    query = makeRequest("GET", url, authenticated_user=True)
    unverified_seism = query.json()

    if not form.is_submitted():

        # If the form is not sent, makes a request
        if query.status_code == 404:
            flash("Seism not found", "warning")
            return redirect(url_for('u_seism.main'))

        form.depth.data = unverified_seism["depth"]
        form.magnitude.data = unverified_seism["magnitude"]

    if form.validate_on_submit():
        seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data
        }
        seism_json = json.dumps(seism)

        query = makeRequest("PUT", url, authenticated_user=True, data=seism_json)
        return redirect(url_for('u_seism.main'))

    return render_template('/derived/unverified-seisms/edit-useism.html', id=id, form=form,
                           unverified_seism=unverified_seism)


@u_seism.route('/delete/<int:id>')
@login_required
def delete_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("DELETE", url, authenticated_user=True)
    if query.status_code == 409:
        flash("Seism not found", "warning")
        return redirect(url_for('u_seism.main'))
    return redirect(url_for('u_seism.main'))


@u_seism.route('/view/<int:id>')
@login_required
def view_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:
        flash("Seism not found", "warning")
        return redirect(url_for('u_seism.main'))
    unverified_seism = query.json()
    return render_template('/derived/unverified-seisms/view-useism.html', unverified_seism=unverified_seism)


@u_seism.route('/validate/<int:id>')
@login_required
def verify_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:
        flash("Seism not found", "warning")
        return redirect(url_for('u_seism.main'))

    verification = {
        "verified": True
    }
    data_json = json.dumps(verification)
    _query = makeRequest("PUT", url, authenticated_user=True, data=data_json)

    return redirect(url_for('u_seism.main'))
