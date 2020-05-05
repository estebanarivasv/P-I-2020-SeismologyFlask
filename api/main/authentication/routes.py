from main.models import UserModel
from main import db

from flask import request, Blueprint
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    entered_email = str(request.get_json().get('email'))
    entered_password = str(request.get_json().get('password'))
    user = db.session.query(UserModel).filter(UserModel.email == entered_email).first_or_404()

    passwords_match = user.validate_password(entered_password)
    # True value if both passwords match

    if passwords_match:
        access_token = create_access_token(identity=user)
        data = {"id": "'+str(user.id_num)+'",
                "email": "'+str(user.email)+'",
                "access_token": "'+access_token+'"
                }
        return data, 200
    else:
        return 'You have entered wrong credentials.', 401


"""
I did not create the /register route because the administrators only activate or deactivate
seismologists accounts.
"""
