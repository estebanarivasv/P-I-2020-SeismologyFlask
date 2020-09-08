from main import login_manager
from flask import request
from flask_login import UserMixin, LoginManager
from jwt import decode, exceptions


class LoggedUser(UserMixin):
    # This class represents the user which is logged in

    def __init__(self, id, email, admin):
        self.id = id
        self.email = email
        self.admin = admin

@login_manager.request_loader
def load_user(request):
    if 'access_token' in request.cookies:
        try:
            decoded_token = decode(request.cookies['access_token'], verify=False)  # Api and web don't have the same password that's why we won't verify
            user_data = decoded_token['user_claims']
            user = LoggedUser(
                id=user_data['id_num'],
                email=user_data['email'],
                admin=user_data['admin']
            )
            return user
        except exceptions.DecodeError as e:
            print(f"JWT exception: {e}")
        except exceptions.InvalidTokenError as e:
            print(f"JWT exception: {e}")
    return None



