from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, url_prefix='/administrator')


@admin.route('/logout/')
def logout():
    pass


@admin.route('/home/')
def index():
    return render_template('derivied/admin/home.html')



@admin.route('/verified-seisms/')
def main_vseism():
    return render_template('/derivied/admin/verified-seisms/main.html')


@admin.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    return render_template('/derivied/admin/verified-seisms/view-vseism.html')


@admin.route('/sensors/')
def main_sensors():
    return render_template('/derivied/admin/sensors/main.html')


@admin.route('/sensors/view/<int:id>')
def view_sensor(id):
    return render_template('/derivied/admin/sensors/view-sensor.html')


@admin.route('/sensors/edit/<int:id>')
def edit_sensor(id):
    return render_template('/derivied/admin/sensors/edit-sensor.html')


@admin.route('/sensors/add/')
def add_sensor():
    return render_template('/derivied/admin/sensors/add-sensor.html')


@admin.route('/users/')
def main_users():
    return render_template('/derivied/admin/users/main.html')


@admin.route('/users/edit/<int:id>')
def edit_user(id):
    return render_template('/derivied/admin/users/edit-user.html')


@admin.route('/users/add/')
def add_user():
    return render_template('/derivied/admin/users/add-user.html')

