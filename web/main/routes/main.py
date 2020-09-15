from flask import Blueprint, redirect, url_for

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return redirect(url_for('user.main_vseisms'))