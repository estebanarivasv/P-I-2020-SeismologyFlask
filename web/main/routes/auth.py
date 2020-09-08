from flask import Blueprint, render_template, redirect, url_for, current_app, request, make_response, flash
from flask_login import login_user, logout_user, current_user
from functools import wraps
import requests
import json

from main.forms import LoginForm
from main.utilities import LoggedUser


auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/login', methods=["POST","GET"])
def login():
    url = current_app.config['API_URL'] + '/auth/login'
    login_form = LoginForm()

    if login_form.validate_on_submit():
        data = {
            "email": login_form.email.data,
            "password": login_form.password.data
        }
        print(F"\n\nJSON DUMPS: {json.dumps(data)}\n\n")
        r = requests.post(url=url, headers={'content-type': 'application/json'}, data=json.dumps(data))

        if r.status_code == 200:
            user_json = json.loads(r.text)
            print(F"\n\nJSON LOADS: {json.loads(r.text)}\n\n")
            logged_user = LoggedUser(
                id=user_json['id_num'],
                email=user_json['email'],
                admin=user_json['admin']
            )
            login_user(logged_user)  # Logs in the user
            print(user_json['admin'])
            if user_json['admin'] == True:
                req = make_response(redirect(url_for('admin.index')))  # Redirection request
                req.set_cookie('access_token', user_json['token'], httponly=True)
                return req
            elif user_json['admin'] == False:
                req = make_response(redirect(url_for('seismologist.index')))  # Redirection request
                req.set_cookie('access_token', user_json['token'], httponly=True)
                return req
        else:
            flash("Unknown credentials. Please try again.", 'danger')
            
    return render_template('/derived/unlogged-usr/log-in.html', login_form=login_form)


@auth.route('/logout')
def logout():
    print("Entro")
    req = make_response(redirect(url_for('unlogged_usr.index')))  # Redirection request
    req.set_cookie('access_token', '', httponly=True)  # Empty cookie and set expiration date in past
    logout_user()
    return req

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.admin:
            flash('You are not authorized to enter to this site.', 'warning')
            return redirect(url_for('seismologist.index'))
        return fn(*args, **kws)
    return wrapper