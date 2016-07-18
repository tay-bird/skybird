""" Serve the splash page. """

from flask import render_template

from interface import app

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/preview")
def preview():
	return render_template('preview.html')
