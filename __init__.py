#!/home/taybird/www/venv/bin/python

from flask import Flask
from flask.ext.stormpath import StormpathManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '***REMOVED***'
app.config['STORMPATH_API_KEY_FILE'] = '/home/taybird/www/keys/apiKey.properties'
app.config['STORMPATH_APPLICATION'] = '***REMOVED***'

app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_ENABLE_REGISTRATION'] = False

#app.config['SECRET_KEY'] = '***REMOVED***'
#app.config['STORMPATH_API_KEY_ID'] = "***REMOVED***"
#app.config['STORMPATH_API_KEY_SECRET'] = "***REMOVED***"
#app.config['STORMPATH_APPLICATION'] = '***REMOVED***'

user_manage = StormpathManager(app)

import views
import interface.views

if __name__ == "__main__":
    app.run()
