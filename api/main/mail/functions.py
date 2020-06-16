from main import out_server_sender as mail_sender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException


def send_mail(to, subject, template_directory, **kwargs):
    sender = current_app.config['FLASKY_MAIL_SENDER']
    msg = Message(subject=subject, sender=sender, recipients=[to])
    try:
        # Plain text body template configuration. **kwargs are used by Jinja to display different templates
        msg.body = render_template(template_directory + '.txt', **kwargs)
        
        # HTML body template configuration.
        msg.html = render_template(template_directory + '.html', **kwargs)
        
        mail_sender.send(msg)
        
    except SMTPException:
        print(SMTPException)
        return 'Mail deliver failure'
    return True
