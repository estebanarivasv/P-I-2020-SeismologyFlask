from flask_wtf import CSRFProtect
from flask_login import LoginManager

login_manager = LoginManager()

csrf = CSRFProtect()