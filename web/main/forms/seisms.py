from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.fields.html5 import DateTimeLocalField as DatetimeField

class Seism(FlaskForm):
        
    depth = wtf.IntegerField(
        label="Depth",
        validators=[wtf.validators.DataRequired(message="This field should be an integer")]
    )
    magnitude = wtf.FloatField(
        label="Magnitude",
        validators=[wtf.validators.DataRequired(message="This field should be a decimal value")]
    )
    submit_button = wtf.SubmitField(label="Save")


class USeismsFilterForm(FlaskForm):
    sensor_id = wtf.SelectField(
        label="Sensor name",
        validators=[wtf.validators.optional()],
        coerce=int)
    from_datetime = DatetimeField(
        label="From date",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%dT%H:%M'
        )
    to_datetime = DatetimeField(
        label="To date",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%dT%H:%M'
        )
    submit_button = wtf.SubmitField(label="Apply")


class VSeismFilter(FlaskForm):
    from_datetime = wtf.DateTimeField(
        label="From date",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
        )
    to_datetime = wtf.DateTimeField(
        label="To date",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
        )
    datetime = wtf.DateTimeField(
        label="Datetime",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
        )
    magnitude = wtf.FloatField(
        label="Magnitude",
        validators=[wtf.validators.optional()]
        )
    sensor_name = wtf.SelectField(
        label="Associated seismologist",
        validators=[wtf.validators.optional()],
        coerce=int)
    submit_button = wtf.SubmitField(label="Apply filters")
