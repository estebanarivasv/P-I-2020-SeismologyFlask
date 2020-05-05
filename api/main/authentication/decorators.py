from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


# We define this decorator in order to restrict the methods that are only accessed by the administrators
def admin_logon_required(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()                         # We verify if the token entered is valid
        claims = get_jwt_claims()                       # We fetch the JWT claims

        if claims['admin']:
            return method(*args, **kwargs)              # If the logged user is an admin, we execute the method
        else:
            return 'You are not allowed to access to this information', 403

    return wrapper
