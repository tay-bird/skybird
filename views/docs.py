""" Serve the document manager. """

import os

from flask import render_template, url_for, request, redirect
from flask.ext.stormpath import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from interface import app, config

config = config["DOC_MANAGER"]
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["UPLOADS_FOLDER"] = config["UPLOADS_FOLDER"]

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    """ Check for a valid file type. """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/docs", methods=['GET', 'POST'])
@login_required
def docs():
    """ Serve the upload page and accept uploads. """
    if request.method == 'POST':
        print request.form['name']
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
            return redirect(url_for('docs'))
    return render_template('docs.html')

@app.route("/upload")
@login_required
def upload():
    return render_template('docs.html')
