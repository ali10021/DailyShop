from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash ,jsonify
from werkzeug.utils import secure_filename
from random import random, randint
from app import routes
from flask_mail import Mail, Message

def app_create():
    app = Flask(__name__)

    app.config.from_object('app.config')
    app.secret_key = app.config["SECRET_KEY"]
    # app.secret_key = "gfsjhfg-87t678564786"

    mail = Mail(app)

    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ahmed345amjad@gmail.com'
    app.config['MAIL_PASSWORD'] = 'bitf18a002'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    app.run(debug=True)
    return app
otp = randint(000000, 999999)
app=app_create()
