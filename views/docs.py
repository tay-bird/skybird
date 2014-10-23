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
        try:
            type = name.rsplit('.', 1)[1]
        except IndexError:
            type = ''
        files.append({ 'size': os.path.getsize(path)/1024,
                       'type': type,
                       'name': name.rsplit('.', 1)[0] })
    
    return render_template('docs.html', location='', files=files)

@app.route("/docs/<directory>")
@login_required
def docs_subdir(directory):
    """ Serve the subdirectory page. """
    files = []
    filenames = os.listdir(os.path.join(app.config["UPLOADS_FOLDER"], directory))
        
    for name in filenames:
        path = os.path.join(app.config["UPLOADS_FOLDER"], directory, name)
        try:
            type = name.rsplit('.', 1)[1]
        except IndexError:
            type = ''
        files.append({ 'size': os.path.getsize(path)/1024,
                       'type': type,
                       'name': name.rsplit('.', 1)[0] })
    
    loc = ''
    if directory:
        loc ='/' + directory
    
    return render_template('docs.html', location=loc, files=files)

@app.route("/docs/upload", methods=['GET', 'POST'])
@app.route("/docs/upload/<directory>", methods=['GET', 'POST'])
@login_required
def upload(directory=None):
    """ Serve the upload page and accept uploads. """
    if request.method == 'POST':
        file = request.files['file']
        
        # Check if a valid file was uploaded. If not, render the 
        # upload page.
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Upload to the correct directory.
            if directory:
                file.save(os.path.join(app.config['UPLOADS_FOLDER'],
                                       directory, filename))
            else:
                file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
            return redirect(url_for('docs'))
        
    loc = ''
    if directory:
        loc = '/' + directory
        
    return render_template('upload.html', location=loc)

@app.route('/docs/new', methods=['POST'])
@login_required
def new():
    """ Create a new directory. """
    name = request.form['name']
    
    path = os.path.join(app.config['UPLOADS_FOLDER'], name)
    
    try:
        os.makedirs(path)
    except OSError:
        pass
    
    return redirect(url_for('docs'))
    
@app.route('/docs/delete')
@login_required
def delete():
    """ Create a new directory. """
    return redirect(url_for('docs'))

@app.route('/docs/view/<filename>/')
@login_required
def view_file(filename):
    """ Display the specified file. """
    return send_from_directory(app.config['UPLOADS_FOLDER'],
                               secure_filename(filename))

@app.route('/docs/get/<filename>/')
@login_required
def get_file(filename):
    """ Send the specified file. """
    return send_from_directory(app.config['UPLOADS_FOLDER'],
                               secure_filename(filename),
                               as_attachment=True)
