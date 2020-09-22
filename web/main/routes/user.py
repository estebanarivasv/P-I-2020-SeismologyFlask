from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from flask_login import login_required
import requests, json

from main.utilities.api_querying import makeRequest

import main.forms as f
from main.routes.auth import admin_required


user = Blueprint('user', __name__, url_prefix='/')


# Administrator's home
@user.route('/admin/')
@login_required
@admin_required
def admin_index():
    return render_template('derived/admin-home.html')

# Seismologist's home
@user.route('/')
@login_required
def seismologist_index():
    return render_template(url_for('user.main_useisms'))

"""
-----------------------------------------------------------------------------
                                  U S E R S
-----------------------------------------------------------------------------
"""
@user.route('/users/')
@login_required
@admin_required
def main_users():
    url = current_app.config["API_URL"] + "/users"
    query = makeRequest("GET", url, authenticated_user=True)
    users = json.loads(query.text)["users"]
    return render_template('/derived/users/main.html', users=users)


@user.route('/users/add/', methods=["POST", "GET"])
@login_required
@admin_required
def add_user():
    url = current_app.config["API_URL"] + "/users"
    form = f.NewUserForm()

    if form.validate_on_submit():
        """
        If form is validated and submitted, we make a POST request to add an user.
        """
        if form.admin.data == "false":
            form.admin.data = False
        else:
            form.admin.data = True
        user = {
            "email" : form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        user_json = json.dumps(user)
        makeRequest("POST", url, authenticated_user=True, data=user_json)
        
        return redirect(url_for('user.main_users'))
        
    return render_template('/derived/users/add-user.html', form=form)

@user.route('/users/edit/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def edit_user(id):
    form = f.UserToEditForm()
    url = current_app.config["API_URL"] + "/user/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if not form.is_submitted():
        """
        If form is not submitted, we store the query.text data from the GET request inside the form's parameters.
        """
        if query.status_code == 404:
            flash("User not found", "warning")
            return redirect(url_for('user.main_users'))
        
        # Saving the json to a Python dict in order to show it for editing
        user = query.json()
        if user["admin"] == False:
            form.admin.data = 0
        else:
            form.admin.data = 1

        form.email.data = user["email"]
        form.admin.data = user["admin"]
    
    
    if form.validate_on_submit():
        """
        Once it is validated and submitted, we store the form's parameters data inside the json for the GET request.
        """
        if form.admin.data == 0:
            form.admin.data = False
        else:
            form.admin.data = True
        user = {
            "email": form.email.data,
            "admin": form.admin.data
        }
        user_data = json.dumps(user)

        makeRequest("PUT", url, authenticated_user=True, data=user_data)
        return redirect(url_for('user.main_users'))

    return render_template('/derived/users/edit-user.html', id=id, form=form, user=query.json())

@user.route('/users/delete/<int:id>')
@login_required
@admin_required
def delete_user(id):
    url = current_app.config["API_URL"] + "/user/" + str(id)
    data = makeRequest("DELETE", url, authenticated_user=True)
    if data.status_code == 409:
        flash("User not found", "warning")
        return redirect(url_for('user.main_users'))
    return redirect(url_for('user.main_users'))

"""
-----------------------------------------------------------------------------
                                S E N S O R S
-----------------------------------------------------------------------------
"""
@user.route('/sensors/')
@login_required
@admin_required
def main_sensors():
    url = current_app.config["API_URL"] + "/sensors"
    query = makeRequest("GET", url, authenticated_user=True)
    sensors = json.loads(query.text)["sensors"]
    return render_template('/derived/sensors/main.html', sensors=sensors)

@user.route('/sensors/add/', methods=["POST", "GET"])
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
        return redirect(url_for('user.main_sensors'))
        
    return render_template('/derived/sensors/add-sensor.html', form=form)

@user.route('/sensors/edit/<int:id>', methods=["POST", "GET"])
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
            return redirect(url_for('admin.main_sensors'))
        
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
        return redirect(url_for('user.main_sensors'))

    return render_template('/derived/sensors/edit-sensor.html', id=id, form=form)

@user.route('/sensors/delete/<int:id>')
@login_required
@admin_required
def delete_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    query = makeRequest("DELETE", url, authenticated_user=True)
    if query.status_code == 409:
        flash(query.text.replace('"', ''), "danger")
        return redirect(url_for('user.main_sensors'))
    else:
        return redirect(url_for('user.main_sensors'))

@user.route('/sensors/view/<int:id>')
@login_required
@admin_required
def view_sensor(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:
        flash("Sensor not found", "warning")
        return redirect(url_for('user.main_sensors'))    
    sensor = query.json()
    return render_template('/derived/sensors/view-sensor.html', sensor=sensor)

@user.route('/sensors/email')
@login_required
@admin_required
def send_emails():
    url = current_app.config["API_URL"] + "/sensors/status"
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 200:
        flash("Email sent to administrators", "success")
    return redirect(url_for('user.main_sensors'))

"""
-----------------------------------------------------------------------------
                        V E R I F I E D   S E I S M S
-----------------------------------------------------------------------------
"""
@user.route('/verified-seisms/')
def main_vseisms():
    url = current_app.config["API_URL"] + "/verified-seisms"
    query = makeRequest("GET", url)
    verified_seisms = json.loads(query.text)["verified_seisms"]
    return render_template('/derived/verified-seisms/main.html', verified_seisms=verified_seisms)

@user.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    url = current_app.config["API_URL"] + "/verified-seism/" + str(id)
    query = makeRequest("GET", url)
    if query.status_code == 404:
        flash("Seism not found", "warning")
        return redirect(url_for('user.main_vseisms'))  
    v_seism = json.loads(query.text)
    return render_template('/derived/verified-seisms/view-vseism.html', v_seism=v_seism)


"""
-----------------------------------------------------------------------------
                    U N V E R I F I E D   S E I S M S
-----------------------------------------------------------------------------
"""
@user.route('/unverified-seisms/')
@login_required
def main_useisms():
    url = current_app.config["API_URL"] + "/unverified-seisms"
    sensors_url = current_app.config["API_URL"] + "/sensors"

    filters = f.USeismsFilterForm(request.args, meta={'csrf': False})
    
    query = makeRequest("GET", sensors_url, authenticated_user=True)
    sensors = json.loads(query.text)["sensors"]

    filters.sensor_id.choices = [(int(sensor['id_num']), sensor['name']) for sensor in sensors]
    filters.sensor_id.choices.insert(0, [0, "-"])

    data = {}
    
    print("\n\nfrom_datetime", filters.from_datetime.data)

    if filters.validate():
        if filters.sensor_id.data != None and filters.sensor_id.data != 0:
            data["sensor_id"] = filters.sensor_id.data
        if filters.from_datetime.data != None:
            data["from_date"] = filters.from_datetime.data.strftime('%Y-%m-%d %H:%M:%S')
        if filters.to_datetime.data != None:
            data["to_date"] = filters.to_datetime.data.strftime('%Y-%m-%d %H:%M:%S')
        print("validate", data)

    if 'page_num' in request.args:
        data["page_num"] = request.args.get('page_num','')

    if 'sort_by' in request.args:
        data["sort_by"] = request.args.get('sort_by','')

    data = json.dumps(data)
    print(data)
    query = makeRequest("GET", url, authenticated_user=True, data=data)


    if query.status_code == 200:
        
        unverified_seisms = json.loads(query.text)["unverified_seisms"]
       
        pagination = {}
        pagination["items_num"] = json.loads(query.text)["items_num"]
        pagination["total_pages"] = json.loads(query.text)["total_pages"]
        pagination["page_num"] = json.loads(query.text)["page_num"]

        return render_template('/derived/unverified-seisms/main.html',
                                unverified_seisms=unverified_seisms,
                                filters=filters,
                                pagination=pagination)
    else:
        return redirect(url_for('user.main_useisms'))


@user.route('/unverified-seisms/edit/<int:id>', methods=["POST", "GET"])
@login_required
def edit_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    form = f.SeismForm()
    
    query = makeRequest("GET", url, authenticated_user=True)
    u_seism = query.json()

    if not form.is_submitted():

        # If the form is not sent, makes a request
        if query.status_code == 404:
            flash("Seism not found", "warning")
            return redirect(url_for('user.main_useisms'))
        
        form.depth.data = u_seism["depth"]
        form.magnitude.data = u_seism["magnitude"]

    if form.validate_on_submit():
        seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data
        }
        seism_json = json.dumps(seism)
        
        query = makeRequest("PUT", url, authenticated_user=True, data=seism_json)
        return redirect(url_for('user.main_useisms'))

    return render_template('/derived/unverified-seisms/edit-useism.html', id=id, form=form, u_seism=u_seism)

@user.route('/unverified-seisms/delete/<int:id>')
@login_required
def delete_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("DELETE", url, authenticated_user=True)
    if query.status_code == 409:
            flash("Seism not found", "warning")
            return redirect(url_for('user.main_useisms'))
    return redirect(url_for('user.main_useisms'))

@user.route('/unverified-seisms/view/<int:id>')
@login_required
def view_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:    
        flash("Seism not found", "warning")
        return redirect(url_for('user.main_useisms'))
    u_seism = query.json()
    return render_template('/derived/unverified-seisms/view-useism.html', u_seism=u_seism)

@user.route('/unverified-seisms/validate/<int:id>')
@login_required
def verify_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    query = makeRequest("GET", url, authenticated_user=True)
    if query.status_code == 404:
        flash("Seism not found", "warning")
        return redirect(url_for('user.main_useisms'))

    verification = {
        "verified": True
    }
    data_json = json.dumps(verification)
    query = makeRequest("PUT", url, authenticated_user=True, data=data_json)
    
    return redirect(url_for('user.main_useisms'))

