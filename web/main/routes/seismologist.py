from flask import Blueprint, render_template, current_app, redirect, url_for
from main.forms import SeismForm
from main.forms.seisms import USeismOrganization
import requests, json

seismologist = Blueprint('seismologist', __name__, url_prefix='/seismologist')


@seismologist.route('/')
def index():
    return redirect(url_for('seismologist.main_useisms'))


@seismologist.route('/unverified-seisms/')
def main_useisms():
    url = current_app.config["API_URL"] + "/unverified-seisms"
    org = USeismOrganization()

    """
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
    """
    
    if org.is_submitted():
        organization = json.dumps({
            "sensor_id": org.sensor_id.data,
            "sort_by": org.sort_by.data
        })
        organization_json = json.dumps(organization)
        print(organization_json)
        data = requests.get(url=url, headers={'content-type': 'application/json'}, json=organization_json)
        unverified_seisms = json.loads(data.text)["unverified_seisms"]
        return render_template('/derived/seismologist/unverified-seisms/main.html', unverified_seisms=unverified_seisms, form=org)

    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    unverified_seisms = json.loads(data.text)["unverified_seisms"]
    return render_template('/derived/seismologist/unverified-seisms/main.html', unverified_seisms=unverified_seisms, form=org)


@seismologist.route('/unverified-seisms/view/<int:id>')
def view_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    u_seism = data.json()
    return render_template('/derived/seismologist/unverified-seisms/view-useism.html', u_seism=u_seism)


@seismologist.route('/unverified-seisms/edit/<int:id>', methods=["POST","GET"])
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
def delete_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    requests.delete(url=url, headers={'content-type': 'application/json'})
    return redirect(url_for('seismologist.main_useisms'))

@seismologist.route('/unverified-seisms/validate/<int:id>')
def verify_useism(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    verification = {
        "verified": True
    }
    requests.put(url=url, headers={'content-type': 'application/json'}, json=verification)
    return redirect(url_for('seismologist.main_useisms'))


@seismologist.route('/verified-seisms/')
def main_vseisms():
    url = current_app.config["API_URL"] + "/verified-seisms"
    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    verified_seisms = json.loads(data.text)["verified_seisms"]
    return render_template('/derived/seismologist/verified-seisms/main.html', verified_seisms=verified_seisms)


@seismologist.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    url = current_app.config["API_URL"] + "/verified-seism/" + str(id)
    data = requests.get(url=url, headers={'content-type': 'application/json'})
    v_seism = data.json()
    return render_template('/derived/seismologist/verified-seisms/view-vseism.html', v_seism=v_seism)