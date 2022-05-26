from threading import Thread

import werkzeug
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from werkzeug.exceptions import InternalServerError

from app_context import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "korepetycje33.pl@gmail.com"
app.config['MAIL_PASSWORD'] = "Kor3p3|ycje33.pl"
mail = Mail(app)

JWTManager(app)


def send_message_thread(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise werkzeug.exceptions.NotImplemented


def send_message(subject, sender, recipients, text, html):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body, message.html = text, html
    Thread(target=send_message_thread,
           args=(app, message)).start()
