from main.models import SensorModel, UserModel
from main import db
from main.mail.functions import send_mail

from flask import Blueprint

sensors = Blueprint("sensors", __name__, url_prefix="/sensors")


# Sends an email with the sensors that are not working anymore to the software administrator
@sensors.route('/status', methods=['POST'])
def post():
    stopped_sensors = db.session.query(SensorModel).filter(SensorModel.status == False)
    administrators = db.session.query(UserModel).filter(UserModel.admin == True)
    subject = "Sensors not working at the moment"
    template_directory = "mail/sensors_status"
    for admin in administrators:
        sent = send_mail(admin.email, subject, template_directory, sensors=stopped_sensors)
        if sent:
            return 'The email has been sent.'
        else:
            db.session.rollback()
            return str(sent), 502
    return stopped_sensors.to_json(), 201
