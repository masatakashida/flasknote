from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
import os
from flask_sqlalchemy import SQLAlchemy

class FlaskWithHamlish(Flask):
	jinja_options = ImmutableDict(
		extensions=[HamlishExtension]
	)
app = FlaskWithHamlish(__name__)

db_uri = "sqlite:///" + os.path.join(app.root_path, 'flasknote.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

@app.route('/')
def hello_world():
	entries = Entry.query.all()
	return render_template('index.haml', entries=entries)

# Database
def connect_db():
	db_path = os.path.join(app.root_path, 'flasknote.db')
	rv = sqlite3.connect(db_path)
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()