from main import db


class Seism(db.Model):
    id_num = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    """sensor_id = db.Column(db.Integer, nullable=False)"""

    def __repr__(self):
        return '<Seism %r %r %r>' % (self.magnitude, self.latitude, self.longitude)

    def to_json(self):
        seism_json = {
            """'sensor_id': self.sensor_id"""
            'id_num': self.id_num,
            'datetime': self.datetime,
            'depth': self.depth,
            'magnitude': self.magnitude,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': self.verified
        }
        return seism_json

    @staticmethod
    def from_json(seism_json):
        id_num = seism_json.get('id_num'),
        datetime = seism_json.get('datetime'),
        depth = seism_json.get('depth'),
        magnitude = seism_json.get('magnitude'),
        latitude = seism_json.get('latitude'),
        longitude = seism_json.get('longitude'),
        verified = seism_json.get('verified')
        """sensor_id = seism_json.get('sensor_id')"""
        return Seism(
            """sensor_id=sensor_id""",
            id_num=id_num,
            datetime=datetime,
            depth=depth,
            magnitude=magnitude,
            latitude=latitude,
            longitude=longitude,
            verified=verified
        )
