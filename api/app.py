from main import create_app
from main import db

import os

# Creating Flask app instance
app = create_app()

# Loading app context
app.app_context().push()

# If this script is run, the db is created if not; and the app is run in an specific port
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=os.getenv('PORT'))
