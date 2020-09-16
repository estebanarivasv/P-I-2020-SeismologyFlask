from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.fields.html5 import EmailField

class NewUser(FlaskForm):

    email = EmailField(
        label="Email",
        validators=[
            wtf.validators.DataRequired(message="This field is required"),
            wtf.validators.Email(message="Wrong email format")])
    password = wtf.PasswordField(
        label="Password",
        validators=[
            wtf.validators.DataRequired(message="This field is required"),
            wtf.validators.EqualTo("re_password", message="The passwords must match")])
    re_password = wtf.PasswordField(
        label="Repeat password",
        validators=[
            wtf.validators.DataRequired(message="This field is required")
        ])
    admin_choices = [(1, 'True'), (0, 'False')]
    admin = wtf.RadioField(
        label="Administrator",
        validators=[wtf.validators.InputRequired(message="This field is required")],
        choices=admin_choices,
        coerce=int)
    submit_button = wtf.SubmitField(label="Save")


class UserToEdit(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[
            wtf.validators.DataRequired(message="This field is required"),
            wtf.validators.Email(message="Wrong email format")])
    admin_choices = [(1, 'True'), (0, 'False')]
    admin = wtf.RadioField(
        label="Administrator",
        validators=[wtf.validators.InputRequired(message="This field is required")],
        choices=admin_choices,
        coerce=int)
    submit_button = wtf.SubmitField(label="Save")