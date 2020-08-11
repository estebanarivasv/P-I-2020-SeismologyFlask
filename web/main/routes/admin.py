from flask import Blueprint, render_template, current_app, redirect, url_for
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
    return render_template('/derived/admin/users/main.html')


@admin.route('/users/edit/<int:id>')
def edit_user(id):
    return render_template('/derived/admin/users/edit-user.html')


@admin.route('/users/add/')
def add_user():
    return render_template('/derived/admin/users/add-user.html')
