""" Serve the email client. """

import json
from os import getpid
from time import time

from flask import render_template
from flask.ext.stormpath import login_required

from interface import app, config

@app.route("/email")
@login_required
def email():
    f = open(config["EMAIL"]["MAIL_STORAGE"],"r")
    raw_mail = f.read()
    f.close()
    
    try:
        mail = json.loads(raw_mail)
    except:
        mail = {}
    
    return render_template('email.html', mail=mail)
