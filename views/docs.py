""" Server the document manager. """

from flask import render_template, url_for, request, redirect
from flask.ext.stormpath import login_required
from flask.ext.sqlalchemy import SQLAlchemy

from interface import app
app.config["SQLALCHEMY_DATABASE_URI"] = config["DOC_MANAGER"]["SQLALCHEMY_DATABASE_URI"]
app.config["UPLOADS_FOLDER"] = config["DOC_MANAGER"]["UPLOADS_FOLDER"]

@app.route("/docs", methods=['GET', 'POST'])
@login_required
def docs():
    if request.method == 'POST':
        #save(request.files['upload'])
        return redirect(url_for('docs'))
    return render_template('docs.html')

@app.route("/upload")
@login_required
def upload():
    return render_template('docs.html')
