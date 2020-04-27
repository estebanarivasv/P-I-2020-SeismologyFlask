from main import db
from main.models.User import User


class Sensor(db.Model):
    id_num = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id_num"), nullable=True)
    user = db.relationship("User", back_populates="sensors", uselist=False, single_parent=True)
    seisms = db.relationship("Seism", back_populates="sensor", passive_deletes="all", single_parent=True)

    def __repr__(self):
        return '<Sensor %r >' % self.name

    def to_json(self):
        self.user = db.session.query(User).get(self.user_id)
        # Verifies if the user id exists in the database chart
        try:
            sensor_json = {
                'id_num': self.id_num,
                'name': str(self.name),
                'ip': str(self.ip),
                'port': self.port,
                'status': self.status,
                'active': self.active,
                'user': self.user.to_json()
            }
        except AttributeError:
            sensor_json = {
                'id_num': self.id_num,
                'name': str(self.name),
                'ip': str(self.ip),
                'port': self.port,
                'status': self.status,
                'active': self.active,
                'user_id': self.user_id
            }
        return sensor_json

    @staticmethod
    def from_json(sensor_json):
        new_name = sensor_json.get('name')
        new_ip = sensor_json.get('ip')
        new_port = sensor_json.get('port')
        new_status = sensor_json.get('status')
        new_active = sensor_json.get('active')
        new_user_id = sensor_json.get('user_id')

        return Sensor(
            name=new_name,
            ip=new_ip,
            port=new_port,
            status=new_status,
            active=new_active,
            user_id=new_user_id
        )
