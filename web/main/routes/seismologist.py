from flask import Blueprint, render_template

seismologist = Blueprint('seismologist', __name__, url_prefix='/seismologist')


@seismologist.route('/logout/')
def logout():
    pass


@seismologist.route('/unverified-seisms/')
def main_useisms():
    return render_template('/derivied/seismologist/unverified-seism/main.html')


@seismologist.route('/unverified-seisms/view/<int:id>')
def view_useism(id):
    return render_template('/derivied/seismologist/unverified-seism/view-useism.html')


@seismologist.route('/unverified-seisms/edit/<int:id>')
def edit_useism(id):
    return render_template('/derivied/seismologist/unverified-seism/edit-useism.html')


@seismologist.route('/verified-seisms/')
def main_vseisms():
    return render_template('/derivied/seismologist/verified-seisms/main.html')


@seismologist.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    return render_template('/derivied/seismologist/verified-seisms/view-vseism.html')
     