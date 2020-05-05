from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


# We define this decorator in order to restrict the methods that are only accessed by the administrators
def admin_logon_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if claims['admin']:
            return function(*args, **kwargs)
        else:
            return 'You are not allowed to access to this information', 403

    return wrapper
