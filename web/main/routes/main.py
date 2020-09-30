"""
-----------------------------------------------------------------------------
                                  M A I N
-----------------------------------------------------------------------------
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from main.routes.auth import admin_required


main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def index():
    return redirect(url_for('v_seism.main'))


# Administrator's home
@main.route('/admin/')
@login_required
@admin_required
def admin_index():
    return render_template('derived/admin-home.html')


# Seismologist's home
@main.route('/')
@login_required
def seismologist_index():
    return render_template(url_for('u_seisms.main'))
