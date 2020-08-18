from flask import Blueprint, render_template, redirect, url_for, current_app    
import requests, json
from main.routes.login import login

unlogged_usr = Blueprint('unlogged_usr', __name__, url_prefix='/')


@unlogged_usr.route('/verified-seisms/')
def index():
    url = current_app.config["API_URL"] + "/verified-seisms"
    data = requests.get(url=url, headers={'content-type': 'application/json'}, json={})
    verified_seisms = json.loads(data.text)["verified_seisms"]
    return render_template('/derived/admin/verified-seisms/main.html', verified_seisms=verified_seisms)


@unlogged_usr.route('/verified-seisms/view/<int:id>')
def view_vseism(id):
    return render_template('/derived/unlogged-usr/verified-seisms/view-vseism.html')


@unlogged_usr.route('/login/')
def sign_in():
    return redirect(url_for('login.index'))
