from flask_wtf import FlaskForm
from wtforms import validators, SelectField, IntegerField, FloatField, SubmitField, StringField


class Seism(FlaskForm):
        
    depth = IntegerField(
        label="Depth",
        validators=[validators.DataRequired(message="This field should be an integer")]
    )
    magnitude = FloatField(
        label="Magnitude",
        validators=[validators.DataRequired(message="This field should be a decimal value")]
    )
    submit_button = SubmitField(label="Save")


class USeismOrganization(FlaskForm):
    sensor_id = StringField(label="Sensor identification number")
    sort_by = SelectField(
        label="Sort by",
        choices=[("", "---"), ("datetime[asc]", "Older to newer"), ("datetime[desc]", "Newer to older")],
        coerce=str)
    submit_button = SubmitField(label="Apply")


class SeismSorting(FlaskForm):
    pass


class SeismPagination(FlaskForm):
    pass
