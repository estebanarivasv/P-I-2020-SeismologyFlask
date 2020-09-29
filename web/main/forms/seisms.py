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
        format='%Y-%m-%d %H:%M:%S'
        )
    to_datetime = DatetimeField(
        label="To date",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
        )
    submit_button = wtf.SubmitField(label="Apply")


class VSeismsFilterForm(FlaskForm):
    from_datetime = DatetimeField(
        label="From date",
        validators=[wtf.validators.optional()]
        )
    to_datetime = DatetimeField(
        label="To date",
        validators=[wtf.validators.optional()]
        )
    depth_min = wtf.IntegerField(
        label="Depth min",
        validators=[wtf.validators.optional()]
        )
    depth_max = wtf.IntegerField(
        label="Depth max",
        validators=[wtf.validators.optional()]
        )
    mag_min = wtf.FloatField(
        label="Magnitude min",
        validators=[wtf.validators.optional()]
        )
    mag_max = wtf.FloatField(
        label="Magnitude max",
        validators=[wtf.validators.optional()]
        )
    sensor_name = wtf.StringField(
        label="Associated sensor",
        validators=[wtf.validators.optional()])
    sort_by = wtf.HiddenField()

    elem_per_page = wtf.IntegerField(
        validators=[wtf.validators.optional()]
        )
    submit_button = wtf.SubmitField(label="Apply filters")
    download = wtf.SubmitField(label="Download seisms into CSV")
