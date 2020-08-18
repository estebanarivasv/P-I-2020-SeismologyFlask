from flask import Blueprint, redirect, url_for
from main.routes.unlogged_usr import unlogged_usr

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def index():
    return redirect(url_for('unlogged_usr.index'))
