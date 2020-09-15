from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class NewUser(FlaskForm):

    email = EmailField(
        label="Email",
        validators=[
            validators.DataRequired(message="This field is required"),
            validators.Email(message="Wrong email format")])
    password = PasswordField(
        label="Password",
        validators=[
            validators.DataRequired(message="This field is required"),
            validators.EqualTo("re_password", message="The passwords must match")])
    re_password = PasswordField(
        label="Repeat password",
        validators=[
            validators.DataRequired(message="This field is required")
        ])
    admin_choices = [(1, 'True'), (0, 'False')]
    admin = RadioField(
        label="Administrator",
        validators=[validators.DataRequired(message="This field is required")],
        choices=admin_choices,
        coerce=int)
    submit_button = SubmitField(label="Save")


class UserToEdit(FlaskForm):

    email = EmailField(
        label="Email",
        validators=[
            validators.DataRequired(message="This field is required"),
            validators.Email(message="Wrong email format")])
    admin_choices = [(1, 'True'), (0, 'False')]
    admin = RadioField(
        label="Administrator",
        validators=[validators.InputRequired(message="This field is required")],
        choices=admin_choices,
        coerce=int)
    submit_button = SubmitField(label="Save")