import os
from main import create_app

web = create_app()
web.app_context().push()

if __name__ == '__main__':
    web.run(debug=True, port=os.getenv('PORT'))
