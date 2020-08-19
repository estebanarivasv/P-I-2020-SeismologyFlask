from flask import Blueprint, render_template, current_app, redirect, url_for
from main.forms.users import Users as UsersForm
import requests, json

admin = Blueprint('admin', __name__, url_prefix='/administrator')


@admin.route('/logout/')
def logout():
    pass


@admin.route('/home/')
def index():
    return render_template('derived/admin/home.html')


@admin.route('/verified-seisms/')
def main_vseism():
    url = current_app.config["API_URL"] + "/verified-seisms"
    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    verified_seisms = json.loads(data.text)["verified_seisms"]
    return render_template('/derived/admin/verified-seisms/main.html', verified_seisms=verified_seisms)


@admin.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    url = current_app.config["API_URL"] + "/verified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    v_seism = data.json()
    return render_template('/derived/admin/verified-seisms/view-vseism.html', v_seism=v_seism)


@admin.route('/sensors/')
def main_sensors():
    return render_template('/derived/admin/sensors/main.html')


@admin.route('/sensors/view/<int:id>')
def view_sensor(id):
    return render_template('/derived/admin/sensors/view-sensor.html')


@admin.route('/sensors/edit/<int:id>')
def edit_sensor(id):
    return render_template('/derived/admin/sensors/edit-sensor.html')


@admin.route('/sensors/add/')
def add_sensor():
    return render_template('/derived/admin/sensors/add-sensor.html')


@admin.route('/users/')
def main_users():
    url = current_app.config["API_URL"] + "/users"
    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    users = json.loads(data.text)["users"]
    return render_template('/derived/admin/users/main.html', users=users)


@admin.route('/users/edit/<int:id>')
def edit_user(id):
    return render_template('/derived/admin/users/edit-user.html')


@admin.route('/users/add/', methods=["POST","GET"])
def add_user():
    form = UsersForm()
    if form.validate_on_submit():

        if form.admin.data == "false":
            form.admin.data = False
        else:
            form.admin.data = True
        
        print(form.admin.data)

        user = {
            "email" : form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        user_json = json.dumps(user)
        url = current_app.config["API_URL"] + "/users"
        data = requests.post(url=url, headers={'content-type': 'application/json'}, data=user_json)
        return redirect(url_for('admin.main_users'))
    return render_template('/derived/admin/users/add-user.html', form=form)
