""" Serve the email client. """

import json
from os import getpid
from time import time

from flask import render_template, redirect, url_for
from flask.ext.stormpath import login_required

from interface import app, config

def _read_mail(path):
    """ Open and decode the json file at the specified path. """
    f = open(path,"r")
    raw_mail = f.read()
    f.close()
    
    try:
        mail = json.loads(raw_mail)
    except:
        mail = {}
    
    return mail

@app.route("/email")
@login_required
def email():
    """ Serve the email page. """
    mail = _read_mail(config["EMAIL"]["MAIL_STORAGE"])
    
    # Limit the body of all messages to 100 chars.
    for m in mail:
        if len(m['body']) > 100:
            m['body-short'] = m['body'][:100] + '...'
        else:
            m['body-short'] = m['body']
    
    return render_template('email.html', active='email', mail=mail)

@app.route("/email/send", methods=['POST'])
@login_required   
def send():
    """ Send the email provided by the client. """
    return redirect(url_for('email'))
