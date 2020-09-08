from flask import Blueprint, render_template, current_app, redirect, url_for, request
from flask_login import login_required
from main.forms import SeismForm
from main.forms.seisms import USeismOrganization
import requests, json

seismologist = Blueprint('seismologist', __name__, url_prefix='/seismologist')


@seismologist.route('/')
def index():
    return redirect(url_for('seismologist.main_useisms'))


@seismologist.route('/unverified-seisms/')
@login_required
def main_useisms():
    form = USeismOrganization()
    auth_token = request.cookies['access_token']
    url = current_app.config["API_URL"] + "/unverified-seisms"
    data = requests.get(url=url, headers={'content-type': 'application/json',
                 'authorization': 'Bearer ' + auth_token}, json={})
    unverified_seisms = json.loads(data.text)["unverified_seisms"]
    return render_template('/derived/seismologist/unverified-seisms/main.html', unverified_seisms=unverified_seisms, form=form)


@seismologist.route('/unverified-seisms/view/<int:id>')
@login_required
def view_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    u_seism = data.json()
    return render_template('/derived/seismologist/unverified-seisms/view-useism.html', u_seism=u_seism)


@seismologist.route('/unverified-seisms/edit/<int:id>', methods=["POST", "GET"])
@login_required
def edit_useism(id):
    form = SeismForm()
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    u_seism = data.json()

    if not form.is_submitted():
        # If the form is not sent, makes a request
        if data.status_code == 404:
            return redirect(url_for('seismologist.main_useisms'))
        
        form.depth.data = u_seism["depth"]
        form.magnitude.data = u_seism["magnitude"]

    if form.validate_on_submit():
        seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data
        }
        seism_json = json.dumps(seism)

        data = requests.put(url=url, headers={'content-type': 'application/json'}, data=seism_json)
        return redirect(url_for('seismologist.main_useisms'))

    return render_template('/derived/seismologist/unverified-seisms/edit-useism.html', id=id, form=form, u_seism=u_seism)


@seismologist.route('/unverified-seisms/delete/<int:id>')
@login_required
def delete_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    requests.delete(url=url, headers={'content-type': 'application/json'})
    return redirect(url_for('seismologist.main_useisms'))

@seismologist.route('/unverified-seisms/validate/<int:id>')
@login_required
def verify_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    verification = {
        "verified": True
    }
    requests.put(url=url, headers={'content-type': 'application/json'}, json=verification)
    return redirect(url_for('seismologist.main_useisms'))