from main import db


class User(db.Model):
    """id_num = db.Column(db.Integer, primary_key=True)"""
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Professor: %r %r >' % self.email

    def to_json(self):
        user_json = {
            """"id_num": self.id_num"""
            "email": self.email,
            "password": self.password,
            "admin": self.admin
        }
        return user_json

    @staticmethod
    def from_json(self, user_json):
        """id_num = professor_json.get('id_num')"""
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        return User(
            """id_num = id_num""",
            email=email,
            password=password,
            admin=admin
        )
