from flask.ext.sqlalchemy import SQLAlchemy

from interface import app, config

config = config["DOC_MANAGER"]
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    location = db.Column(db.String(120), unique=True)    
    owner = db.Column(db.String(80))

    def __init__(self, name, owner, location):
        self.name = name
        self.location = location
        self.owner = owner

    def __repr__(self):
        return '<File %r>' % self.name
