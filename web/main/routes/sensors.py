"""
-----------------------------------------------------------------------------
                                S E N S O R S
-----------------------------------------------------------------------------
"""
import json
from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from flask_login import login_required

import main.forms as f
from main.utilities.api_querying import makeRequest
from main.routes.auth import admin_required

sensors_ = Blueprint('sensors', __name__, url_prefix='/sensors/')


@sensors_.route('/')
@login_required
@admin_required
def main():
    url = current_app.config["API_URL"] + "/sensors"
    filters = f.SensorsFilterForm(request.args, meta={'csrf': False})

    query = makeRequest("GET", url, authenticated_user=True)
    sensors = json.loads(query.text)["sensors"]

    data = {}

    if 'name' in request.args and request.args['name'] != "":
        data["name"] = request.args.get('name', '')

    if 'status' in request.args and request.args['status'] != "":
        data["status"] = request.args.get('status', '')

    if 'active' in request.args and request.args['active'] != "":
        data["active"] = request.args.get('active', '')

    if 'user_email' in request.args and request.args['user_email'] != "":
        data["user_email"] = request.args.get('user_email', '')

    if 'sort_by' in request.args and request.args['sort_by'] != "":
        data["sort_by"] = request.args.get('sort_by', '')

    if 'page_num' in request.args and request.args['page_num'] != "":
        data["page_num"] = request.args.get('page_num', '')
        
    if 'elem_per_page' in request.args and request.args['elem_per_page'] != "":
        data["elem_per_page"] = request.args.get('elem_per_page', '')


    data = json.dumps(data)
    query = makeRequest("GET", url, authenticated_user=True, data=data)

    if query.status_code == 200:
        sensors = json.loads(query.text)["sensors"]

        pagination = {"items_num": json.loads(query.text)["items_num"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page_num": json.loads(query.text)["page_num"]}

        return render_template('/derived/sensors/main.html',
                               sensors=sensors,
                               filters=filters,
                               pagination=pagination)

    else:
        return redirect(url_for('sensors.main'))


@sensors_.route('/add/', methods=["POST", "GET"])
@login_required
@admin_required
def add_sensor():
    url = current_app.config["API_URL"] + "/sensors"
    form = f.NewSensorForm()

    """
    We make a GET request to achieve the user emails and append them to the user_id.choices of the form
    """
    users_url = current_app.config["API_URL"] + "/users"
    u_data = makeRequest("GET", users_url, authenticated_user=True)
    user_json = json.loads(u_data.text)

    email_list = [(0, "Select one seismologist email")]
    for user in user_json["users"]:
        email_list.append((user["id_num"], user["email"]))
    form.user_id.choices = email_list

    if form.validate_on_submit():
        """
        Once it is validated and submitted, we store the form's parameters data inside the json for the POST request.
        """
        if form.status.data == 0:
            form.status.data = False
        else:
            form.status.data = True

        if form.active.data == 0:
            form.active.data = False
        else:
            form.active.data = True

        u_id = form.user_id.data

        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "user_id": u_id
        }
        sensor_json = json.dumps(sensor)

        u_data = makeRequest("POST", url, authenticated_user=True, data=sensor_json)
        return redirect(url_for('sensors.main'))

    return render_template('/derived/sensors/add-sensor.html', form=form)


@sensors_.route('/edit/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def edit_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    form = f.NewSensorForm()

    """
    We make a GET request to achieve the user emails and append them to the user_id.choices of the form
    """
    users_url = current_app.config["API_URL"] + "/users"
    u_data = makeRequest("GET", users_url, authenticated_user=True)
    user_json = json.loads(u_data.text)
    email_list = [(0, "Select one seismologist email")]
    for user in user_json["users"]:
        email_list.append((int(user["id_num"]), user["email"]))
    form.user_id.choices = email_list

    if not form.is_submitted():
        """
        If form is not submitted, we store the data.json() from the GET request inside the form's parameters.
        """
        data = makeRequest("GET", url, authenticated_user=True)

        if data.status_code == 404:
            flash("Sensor not found", "warning")
            return redirect(url_for('sensors.main'))

        # Saving the json to a Python dict in order to show it for editing
        sensor = data.json()

        form.name.data = sensor["name"]
        form.ip.data = sensor["ip"]
        form.port.data = sensor["port"]
        if sensor["status"] is False:
            form.status.data = 0
        else:
            form.status.data = 1
        if sensor["active"] is False:
            form.active.data = 0
        else:
            form.active.data = 1

        try:
            if sensor["user_id"] in sensor:
                for id_num, _email in email_list:
                    if id_num == int(sensor["user_id"]):
                        form.user_id.data = int(id_num)
        except KeyError:
            pass

        try:
            user_a = sensor["user"]
            for id_num, _email in email_list:
                if id_num == int(user_a["id_num"]):
                    form.user_id.data = int(id_num)
        except KeyError:
            pass

    if form.validate_on_submit():

        if form.status.data == 0:
            form.status.data = False
        else:
            form.status.data = True
        if form.active.data == 0:
            form.active.data = False
        else:
            form.active.data = True

        u_id = form.user_id.data

        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "user_id": u_id
        }
        sensor_data = json.dumps(sensor)
        u_data = makeRequest("PUT", url, authenticated_user=True, data=sensor_data)
        return redirect(url_for('sensors.main'))

    return render_template('/derived/sensors/edit-sensor.html', id=id, form=form)


@sensors_.route('/delete/<int:id>')
@login_required
@admin_required
def delete_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    query = makeRequest("DELETE", url, authenticated_user=True)
    if query.status_code == 409:
        flash(query.text.replace('"', ''), "danger")
        return redirect(url_for('sensors.main'))
    else:
        return redirect(url_for('sensors.main'))


@sensors_.route('/view/<int:id>')
@login_required
@admin_required
def view_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:
        flash("Sensor not found", "warning")
        return redirect(url_for('sensors.main'))
    sensor = query.json()
    return render_template('/derived/sensors/view-sensor.html', sensor=sensor)


@sensors_.route('/check/<int:id>')
@login_required
@admin_required
def check_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/check/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 409:
        flash(query.text.replace('"', ''), "danger")
        return redirect(url_for('sensors.main'))
    elif query.status_code == 201:
        flash(query.text.replace('"', ''), "success")
        return redirect(url_for('sensors.main'))
    else:
        flash(query.text.replace('"', ''), "success")
        return redirect(url_for('sensors.main'))


@sensors_.route('/email')
@login_required
@admin_required
def send_emails():
    url = current_app.config["API_URL"] + "/sensors/status"
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 200:
        flash("Email sent to administrators", "success")
    return redirect(url_for('sensors.main'))
