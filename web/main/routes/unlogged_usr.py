from flask import Blueprint, render_template, redirect, url_for
from main.routes.login import login

unlogged_usr = Blueprint('unlogged_user', __name__, url_prefix='/')


@unlogged_usr.route('/verified-seisms/')
def index():
    return render_template('/derivied/unlogged-usr/verified-seisms/main.html')


@unlogged_usr.route('/verified-seisms/view/<int:id>')
def view(id):
    return render_template('/derivied/unlogged-usr/verified-seisms/view-vseism.html')


@unlogged_usr.route('/login/')
def sign_in():
    return redirect(url_for('login.index'))
