""" Serve the email client. """

import json
from os import getpid
from time import time

from flask import render_template
from flask.ext.stormpath import login_required

from interface import app

@app.route("/email")
@login_required
def email():	
	f = open("/home/taybird/projects/mailchecker/mail.json","r")
	raw_mail = f.read()
	f.close()
	mail = json.loads(raw_mail)
		
	return render_template('email.html', mail=mail)
