# -*- coding: utf8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID

from config import basedir, ADMINS, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
oid = OpenID(app, os.path.join(basedir, "tmp"))
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'flaskr failure',
                               credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    file_handler = RotatingFileHandler('tmp/flaskr.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('flaskr startup')

from app import views, models
