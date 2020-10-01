"""
-----------------------------------------------------------------------------
                                  U S E R S
-----------------------------------------------------------------------------
"""

import json
from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import login_required

import main.forms as f
from main.routes.auth import admin_required
from main.utilities.api_querying import makeRequest

user_ = Blueprint('user', __name__, url_prefix='/users/')


@user_.route('/')
@login_required
@admin_required
def main():
    url = current_app.config["API_URL"] + "/users"
    query = makeRequest("GET", url, authenticated_user=True)
    users = json.loads(query.text)["users"]
    return render_template('/derived/users/main.html', users=users)


@user_.route('/add/', methods=["POST", "GET"])
@login_required
@admin_required
def add_user():
    url = current_app.config["API_URL"] + "/users"
    form = f.NewUserForm()

    if form.validate_on_submit():
        """
        If form is validated and submitted, we make a POST request to add an user.
        """
        if form.admin.data == 0:
            form.admin.data = False
        else:
            form.admin.data = True
        user = {
            "email": form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        user_json = json.dumps(user)
        makeRequest("POST", url, authenticated_user=True, data=user_json)

        return redirect(url_for('user.main'))

    return render_template('/derived/users/add-user.html', form=form)


@user_.route('/edit/<int:id>', methods=["POST", "GET"])
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
            return redirect(url_for('user.main'))

        # Saving the json to a Python dict in order to show it for editing
        user = query.json()
        if not user["admin"]:
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
        return redirect(url_for('user.main'))

    return render_template('/derived/users/edit-user.html', id=id, form=form, user=query.json())


@user_.route('/delete/<int:id>')
@login_required
@admin_required
def delete_user(id):
    url = current_app.config["API_URL"] + "/user/" + str(id)
    data = makeRequest("DELETE", url, authenticated_user=True)
    if data.status_code == 409:
        flash("User not found", "warning")
        return redirect(url_for('user.main'))
    return redirect(url_for('user.main'))
