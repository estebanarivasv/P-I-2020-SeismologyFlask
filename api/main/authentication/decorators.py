from main import jwt
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


# We declare here the attribute that will be used for the user identification
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id_num


# We declare here the claims that the JWT will store
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'id_num': user.id_num,
        'admin': user.admin
    }


# We define this decorator in order to restrict the methods that are only accessed by the administrators
def admin_login_required(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # We verify if the entered token is valid
        claims = get_jwt_claims()  # We fetch the JWT claims

        if claims['admin']:
            return method(*args, **kwargs)  # If the logged user is an admin, we execute the method
        else:
            return 'You are not allowed to access to this information', 403

    return wrapper
