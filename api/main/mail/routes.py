from main.models import SensorModel, UserModel
from main import db
from main.mail.functions import send_mail

from flask import Blueprint

sensors = Blueprint("sensors", __name__, url_prefix="/sensors")


# Sends an email with the sensors that are not working anymore to the software administrator
@sensors.route('/status', methods=['GET'])
def post():
    stopped_sensors = db.session.query(SensorModel).filter(SensorModel.status == False)
    admins_mail = db.session.query(UserModel.email).filter(UserModel.admin == True)
    subject = "Sensors not working at the moment"
    template_directory = "mail/sensors_status"

    # Turning emails into an array
    recipients = [email for email, in admins_mail]

    for to in recipients:
        sent = send_mail(to, subject, template_directory, sensors=stopped_sensors)
        if not sent:
            break
    try:
        if sent:
            return 'The email/emails has been sent.', 200
        else:
            return str(sent), 502
    
    except Exception as error:
        return str(error), 409
