from main import db


class Sensor(db.Model):
    id_num = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    """user_id = db.Column(db.Integer, db.ForeignKey, nullable=False)"""

    def __repr__(self):
        return '<Sensor %r >' % self.name

    def to_json(self):
        sensor_json = {
            """'user_id': self.user_id"""
            'id_num': self.id_num,
            'name': str(self.name),
            'ip': str(self.ip),
            'port': self.port,
            'status': self.status,
            'active': self.active
        }
        return sensor_json

    @staticmethod
    def from_json(sensor_json):
        id_num = sensor_json.get('id_num')
        name = sensor_json.get('name')
        ip = sensor_json.get('ip')
        port = sensor_json.get('port')
        status = sensor_json.get('status')
        active = sensor_json.get('active')
        user_id = sensor_json.get('user_id')
        return Sensor(
            """user_id = user_id""",
            id_num=id_num,
            name=name,
            ip=ip,
            port=port,
            status=status,
            active=active
        )

