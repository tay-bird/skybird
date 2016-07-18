from flask import url_for, g
from flask import redirect, session, request
from flask.ext.stormpath import login_required, user
from wsgiref.handlers import CGIHandler
from flup.server.fcgi import WSGIServer

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

from skybird import app, config


config = config["CALENDAR"]
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
credential_storage = config["credential_storage"]
callback_uri = config["callback_uri"]

app.config['SECRET_KEY'] = 'secret'

@app.route('/authorize')
@login_required
def authorize():
    """ Authorize the user's Google API session. """
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri=callback_uri,
      approval_prompt='force',
      access_type='offline')

    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

@app.route('/deauthorize')
@login_required
def deauthorize():
    """ Deauthorize the user's Google API session. """
    storage = Storage(credential_storage + user.username + '.dat')
    
    try:
        storage.delete()
    except OSError:
        pass  # No credential file was found.
    
    return redirect(url_for('cal'))

@app.route('/callback')
@login_required
def oauth2callback():
    """ Exchange the authorization code for user credentials. """
    code = request.args.get('code')
    if code:
        flow = OAuth2WebServerFlow(CLIENT_ID,
          CLIENT_SECRET,
          "https://www.googleapis.com/auth/calendar")
        flow.redirect_uri = callback_uri
        try:
            credentials = flow.step2_exchange(code)
        except Exception as e:
            print "Unable to get an access token because ", e.message

        storage = Storage(credential_storage + user.username + '.dat')
        storage.put(credentials)

    return redirect(url_for('cal'))
