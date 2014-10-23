import json
import httplib2

from oauth2client.file import Storage
from apiclient.discovery import build_from_document, build

from flask import render_template, redirect, url_for
from flask.ext.stormpath import login_required, user
from oauth2client.file import Storage
from apiclient.discovery import build_from_document, build

from gcalendar import Gcalendar
from interface import app, config

config = config["CALENDAR"]
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
credential_storage = config["credential_storage"]
callback_uri = config["callback_uri"]

def _gcal_to_resp(events):
    """ Convert Google Cal events to Responsive Cal events. """
    result = events
    
    '''for event in events:
        result.append { "2014-10-30": {"number": 5, "url": "http://w3widgets.com/responsive-calendar"},
                    "2014-10-26": {"number": 1, "url": "http://w3widgets.com"}, 
                    "2014-10-03": {"number": 1}, 
                    "2014-10-12": {}
                } '''
    
    return result

@app.route("/calendar")
@login_required
def cal():
    """ Serve the calendar page. """
    storage = Storage(credential_storage + user.email + '.dat')

    try:
        credentials = storage.get()
    except:
        credentials = None
    
    if credentials:
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build("calendar", "v3", http=http)
        gcalendar = Gcalendar(service)

        events = gcalendar.get_events('primary')
        events = _gcal_to_resp(events)
        
        return render_template('calendar.html', auth=True,
                               events=events)
    else:
        events = {}
        return render_template('calendar.html', auth=False,
                               events=events)
    
@app.route("/calendar/add")
@login_required
def add():
    """ Add the event provided by the client. """
    return redirect(url_for('cal'))
