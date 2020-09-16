from flask_wtf import FlaskForm
import wtforms as wtf

class SortBy(FlaskForm):
    sort_by = wtf.RadioField(
        label="Sort by",
        validators=[wtf.validators.optional()],
        coerce=str)
    submit_button = wtf.SubmitField(label="Apply sorting")
