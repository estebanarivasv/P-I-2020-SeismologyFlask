from flask_wtf import FlaskForm
from wtforms import validators, RadioField, StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField


class NewSensor(FlaskForm):

    name = StringField(
        label="Name",
        validators=[validators.DataRequired(message="This field is required")]
    )
    ip = StringField(
        label="IP Address",
        validators=[validators.DataRequired(message="This field is required")]
    )
    port = IntegerField(
        label="Port",
        validators=[validators.DataRequired(message="This field is required")]
    )
    status_choices = [(1, 'Working'), (0, 'Not-working')]
    status = RadioField(
        label="Status",
        choices=status_choices,
        validators=[validators.InputRequired(message="This field is required")],
        coerce=int
    )
    active_choices = [(1, 'True'), (0, 'False')]
    active = RadioField(
        label="Active",
        choices=active_choices,
        validators=[validators.InputRequired(message="This field is required")],
        coerce=int
    )
    user_id = SelectField(
        label="Associated seismologist",
        validators=[validators.InputRequired(message="This field is required")],
        coerce=int)
    submit_button = SubmitField(label="Save")
