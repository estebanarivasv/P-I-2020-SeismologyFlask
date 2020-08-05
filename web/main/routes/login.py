from flask import Blueprint, render_template

login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/login')
def index():
    return render_template('/derivied/unlogged-usr/log-in.html')
