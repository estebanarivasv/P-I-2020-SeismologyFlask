from flask_wtf import FlaskForm
import wtforms as wtf



class NewSensor(FlaskForm):

    name = wtf.StringField(
        label="Name",
        validators=[wtf.validators.DataRequired(message="This field is required")]
    )
    ip = wtf.StringField(
        label="IP Address",
        validators=[wtf.validators.DataRequired(message="This field is required")]
    )
    port = wtf.IntegerField(
        label="Port",
        validators=[wtf.validators.DataRequired(message="This field is required")]
    )
    status_choices = [(1, 'Working'), (0, 'Not-working')]
    status = wtf.RadioField(
        label="Status",
        choices=status_choices,
        validators=[wtf.validators.InputRequired(message="This field is required")],
        coerce=int
    )
    active_choices = [(1, 'True'), (0, 'False')]
    active = wtf.RadioField(
        label="Active",
        choices=active_choices,
        validators=[wtf.validators.InputRequired(message="This field is required")],
        coerce=int
    )
    user_id = wtf.SelectField(
        label="Associated seismologist",
        validators=[wtf.validators.InputRequired(message="This field is required")],
        coerce=int)
    submit_button = wtf.SubmitField(label="Save")


class SensorsFilterForm(FlaskForm):
    name = wtf.StringField(
        label="Sensor name",
        validators=[wtf.validators.optional()]
    )
    status = wtf.RadioField(
        label="Status",
        choices=[(1, 'Working'), (0, 'Not-working')],
        validators=[wtf.validators.optional()],
        coerce=int
    )
    active = wtf.RadioField(
        label="Active",
        choices=[(1, 'True'), (0, 'False')],
        validators=[wtf.validators.optional()],
        coerce=int
    )
    user_email = wtf.StringField(
        label="User email",
        validators=[wtf.validators.optional()]
    )
    submit_button = wtf.SubmitField(label="Apply filters")
