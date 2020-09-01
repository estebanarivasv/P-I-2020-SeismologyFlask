from flask_wtf import FlaskForm
from wtforms import validators, RadioField, StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField

class NewSensor(FlaskForm):

    name = StringField(
        label="Name",
        validators=[validators.required(message="This field is required")]
    )
    ip = StringField(
        label="IP Address",
        validators=[validators.required(message="This field is required")]
    )
    port = IntegerField(
        label="Port",
        validators=[validators.required(message="This field is required")]
    )
    status_choices = [('true','Working'), ('false','Not-working')]
    status = RadioField(
        label="Status",
        choices=status_choices,
        validators=[validators.required(message="This field is required")]
    )
    active_choices = [('true','True'), ('false','False')]
    active = RadioField(
        label="Active",
        choices=active_choices,
        validators=[validators.required(message="This field is required")]
    )
    user_id = SelectField(
        label="Associated seismologist",
        validators=[validators.required(message="This field is required")],
        coerce=int)
    submit_button = SubmitField(label="Save")
