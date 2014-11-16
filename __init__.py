#!/home/taybird/www/venv/bin/python

import os, json, random, string

from flask import Flask
from flask.ext.stormpath import StormpathManager
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

# Load config.

path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../CONFIG"))
f = open(path)
j = f.read()
f.close()

config = json.loads(j)

# Configure Stormpath.

app.config["SECRET_KEY"] = ''.join(random.choice(string.ascii_letters) for _ in range(32))
app.config["STORMPATH_API_KEY_FILE"] = config["STORMPATH"]["STORMPATH_API_KEY_FILE"]
app.config["STORMPATH_APPLICATION"] = config["STORMPATH"]["STORMPATH_APPLICATION"]

app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_ENABLE_REGISTRATION'] = False

user_manage = StormpathManager(app)

# Configure Flask-Assets.

assets = Environment(app)

js_base = Bundle('js/jquery.js', 'js/bootstrap.js',
                 filters='rjsmin', output='gen/basepack.js')
assets.register('js_base', js_base)

js_calendar = Bundle('js/moment.js', 'js/bootstrap-datetimepicker.js',
                     'js/responsive-calendar.js', filters='jsmin',
                     output='gen/calpack.js')
assets.register('js_calendar', js_calendar)

js_upload = Bundle('js/upload.js', filters='jsmin',
                   output='gen/uplpack.js')
assets.register('js_upload', js_upload)

# Load views.

import views
import interface.views
