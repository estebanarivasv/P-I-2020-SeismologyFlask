from main import db


class User(db.Model):
    id_num = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    sensors = db.relationship("SensorModule", back_populates="user", passive_delete="all")

    def __repr__(self):
        return '<User: %r >' % self.email

    def to_json(self):
        user_json = {
            "id_num": self.id_num,
            "email": self.email,
            "password": self.password,
            "admin": self.admin
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        new_id_num = user_json.get('id_num')
        new_email = user_json.get('email')
        new_password = user_json.get('password')
        new_admin = user_json.get('admin')
        return User(
            id_num=new_id_num,
            email=new_email,
            password=new_password,
            admin=new_admin
        )
