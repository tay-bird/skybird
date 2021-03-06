""" Serve the dashboard. """

import json
from os import getpid
from time import time

from flask import render_template, jsonify
from flask.ext.stormpath import login_required
from psutil import disk_usage, Process, net_connections

from skybird import app, config

@app.route("/dash")
@login_required
def dash():
    """ Serve the dashboard overview. """
    return render_template('dash.html', active='dash')

@app.route("/dash/fetch", methods=['POST'])
@login_required
def dash_fetch():
    """ Fetch the stats and format them as an AJAJ response. """
    # Get Apache uptime. Not currently used. Add to full stat view?
    now = time()
    boot = Process(getpid()).create_time()
    apache_uptime = (now - boot) / 3600  # Convert to hours

    # Get server uptime.
    with open('/proc/uptime', 'r') as f:
        uptime_s = float(f.readline().split()[0])
        uptime = uptime_s / 3600

    # Get disk usage.
    usage = disk_usage('/').percent

    # Get open network connections.
    ip = net_connections()
    cons = []
    for x in ip:
        if x.status is not 'NONE' and x.status is not 'LISTEN':
            con = x.raddr + (x.status,)
            cons.append(con)

    # Get mail count in inbox.
    f = open(config["EMAIL"]["MAIL_STORAGE"], "r")
    mail = f.read()
    f.close()

    try:
        mail_count = len(json.loads(mail))
    except ValueError:
        mail_count = 0
    
    mail_count = 0
    
    stats = { 'uptime': str(uptime)[:5],
              'usage': usage,
              'cons': cons,
              'mail_count': mail_count }
    
    return jsonify(stats)
             
