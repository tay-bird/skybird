#!/home/taybird/www/venv/bin/python

import os, json

from flask import Flask
from flask.ext.stormpath import StormpathManager

app = Flask(__name__)

path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../CONFIG"))
f = open(path)
j = f.read()
f.close()
config = json.loads(j)

app.config["SECRET_KEY"] = "***REMOVED***"
app.config["STORMPATH_API_KEY_FILE"] = config["STORMPATH"]["STORMPATH_API_KEY_FILE"]
app.config["STORMPATH_APPLICATION"] = config["STORMPATH"]["STORMPATH_APPLICATION"]

app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_ENABLE_REGISTRATION'] = False

user_manage = StormpathManager(app)

import views
import interface.views

if __name__ == "__main__":
    app.run()
