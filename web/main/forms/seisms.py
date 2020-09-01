from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class Seism(FlaskForm):
    

    """
    id_num = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id_num', ondelete="RESTRICT"), nullable=False)
    sensor = db.relationship("Sensor", back_populates="seisms", uselist=False, passive_deletes="all", single_parent=True)
    """