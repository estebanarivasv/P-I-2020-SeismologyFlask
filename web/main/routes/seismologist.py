from flask import Blueprint, render_template, current_app
import requests, json

seismologist = Blueprint('seismologist', __name__, url_prefix='/seismologist')


@seismologist.route('/logout/')
def logout():
    pass


@seismologist.route('/unverified-seisms/')
def main_useisms():
    url = current_app.config["API_URL"] + "/unverified-seisms"
    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    unverified_seisms = json.loads(data.text)["unverified_seisms"]
    print("devol\n\n", unverified_seisms)
    return render_template('/derived/seismologist/unverified-seisms/main.html', unverified_seisms=unverified_seisms)


@seismologist.route('/unverified-seisms/view/<int:id>')
def view_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    u_seism = data.json()
    return render_template('/derived/seismologist/unverified-seisms/view-useism.html', u_seism=u_seism)


@seismologist.route('/unverified-seisms/edit/<int:id>')
def edit_useism(id):
    return render_template('/derived/seismologist/unverified-seism/edit-useism.html')


@seismologist.route('/verified-seisms/')
def main_vseisms():
    return render_template('/derived/seismologist/verified-seisms/main.html')


@seismologist.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    return render_template('/derived/seismologist/verified-seisms/view-vseism.html')
     