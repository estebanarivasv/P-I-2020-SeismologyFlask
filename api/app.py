from main import create_app
from main import db
from main.models import UserModel

import os


def create_admins_in_db():
    admins = db.session.query(UserModel.id_num).filter(UserModel.admin == True)
    admins_list = [admin for admin, in admins]
    if len(admins_list) == 0:
        print("Creando admin")
        user = UserModel(
            email=os.getenv('ADMIN_MAIL'),
            plain_password=os.getenv('ADMIN_PLAIN_PASSWORD'),
            admin=bool(os.getenv('ADMIN_BOOL'))
        )
        db.session.add(user)
        db.session.commit()

    else:
        pass


# Creating Flask app instance
app = create_app()

# Loading app context
app.app_context().push()

# If this script is run, the db is created if not; and the app is run in an specific port
if __name__ == '__main__':
    db.create_all()
    create_admins_in_db()
    app.run(debug=True, port=os.getenv('PORT'))
