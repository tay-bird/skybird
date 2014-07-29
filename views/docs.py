""" Serve the document manager. """

import os

from flask import render_template, url_for, request
from flask import send_from_directory, redirect
from flask.ext.stormpath import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from interface import app, config

config = config["DOC_MANAGER"]
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["UPLOADS_FOLDER"] = config["UPLOADS_FOLDER"]
app.config['MAX_CONTENT_LENGTH'] = config["MAX_SIZE_IN_MB"] * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def _allowed_file(filename):
    """ Check for a valid file type. """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/docs")
@login_required
def docs():
    """ Serve the document manager overview page. """
    files = []
    filenames = os.listdir(app.config["UPLOADS_FOLDER"])
        
    for name in filenames:
        path = os.path.join(app.config["UPLOADS_FOLDER"], name)
        files.append({ 'size': os.path.getsize(path)/1024,
                       'type': name.rsplit('.', 1)[1],
                       'name': name.rsplit('.', 1)[0] })
    
    return render_template('docs.html', files=files)

@app.route("/docs/upload", methods=['GET', 'POST'])
@login_required
def upload():
    """ Serve the upload page and accept uploads. """
    if request.method == 'POST':
        file = request.files['file']
        
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
            return redirect(url_for('docs'))
            
    return render_template('upload.html')

@app.route('/docs/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_FOLDER'],
                               secure_filename(filename))
