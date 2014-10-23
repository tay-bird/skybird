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

@app.route("/calendar")
@login_required
def cal():
    """ Serve the calendar page. """
    storage = Storage(credential_storage + user.email + '.dat')

    try:
        credentials = storage.get()
    except:
        credentials = None

    if credentials == None or credentials.invalid:
        return redirect(url_for('authorize'))

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build("calendar", "v3", http=http)
    gcalendar = Gcalendar(service)

    tasks_cal = gcalendar.get_calendar_id('gcal_tasks')
    appts_cal = gcalendar.get_calendar_id('gcal_appts')
    
    return render_template('calendar.html')
