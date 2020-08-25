from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField


"""admin
email
password
confirm """

class Users(FlaskForm):
    email = EmailField('E-mail',
    [
        validators.Required(message="An email is required"),
        validators.Email(message="The format is not valid")
    ])

    password = PasswordField('Password', [
        validators.Required(message="The password is mandatory"),
        validators.EqualTo('confirm', message="Passwords don't match")
    ])

    confirm = PasswordField("Repeat password")

    admin_list = [
        ('true','True'),
        ('false','False'),
    ]

    admin = RadioField('Admin', choices=admin_list, default='false')
    
    submit = SubmitField("Send")


class UsersEdit(FlaskForm):
    email = EmailField('E-mail',
    [
        validators.Required(message="An email is required"),
        validators.Email(message="The format is not valid")
    ])

    admin_list = [
        ('true','True'),
        ('false','False'),
    ]

    admin = RadioField('Admin', choices=admin_list, default='false')
    
    submit = SubmitField("Send")


    