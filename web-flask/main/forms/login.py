from flask_wtf import FlaskForm
from wtforms import validators, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField

class Login(FlaskForm):

    email = EmailField(
        label="Email address",
        validators=[
            validators.DataRequired(message="This field is required"),
            validators.Email(message="Wrong email format")])
    password = PasswordField(
        label="Password",
        validators=[
            validators.DataRequired(message="This field is required")])
    submit_button = SubmitField(label="Sign in")