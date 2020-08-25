from main import db
from main.models.Sensor import Sensor
import datetime as dt


class Seism(db.Model):
    id_num = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id_num', ondelete="RESTRICT"), nullable=False)
    sensor = db.relationship("Sensor", back_populates="seisms", uselist=False, passive_deletes="all",
                             single_parent=True)

    def __repr__(self):
        return '<Seism %r %r %r>' % (self.magnitude, self.latitude, self.longitude)

    def to_json(self):
        self.sensor = db.session.query(Sensor).get_or_404(self.sensor_id)
        # Verifies if the sensor does exist in the database chart
        seism_json = {
            'id_num': self.id_num,
            'datetime': self.datetime.isoformat(),
            'depth': self.depth,
            'magnitude': self.magnitude,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': self.verified,
            'sensor': self.sensor.to_json()
        }
        return seism_json

    def to_json_public(self):
        self.sensor = db.session.query(Sensor).get_or_404(self.sensor_id)
        # Verifies if the sensor does exist in the database chart
        seism_json = {
            'id_num': self.id_num,
            'datetime': self.datetime.isoformat(' '),
            'depth': self.depth,
            'magnitude': self.magnitude,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': self.verified,
            'sensor': self.sensor.to_json()
        }
        return seism_json

    @staticmethod
    def from_json(seism_json):
        new_datetime = dt.datetime.strptime(seism_json.get('datetime'), "%Y-%m-%dT%H:%M:%S"),
        new_depth = seism_json.get('depth')
        new_magnitude = seism_json.get('magnitude')
        new_latitude = seism_json.get('latitude')
        new_longitude = seism_json.get('longitude')
        new_verified = seism_json.get('verified')
        new_sensor_id = seism_json.get('sensor_id')

        return Seism(
            datetime=new_datetime,
            depth=new_depth,
            magnitude=new_magnitude,
            latitude=new_latitude,
            longitude=new_longitude,
            verified=new_verified,
            sensor_id=new_sensor_id
        )
