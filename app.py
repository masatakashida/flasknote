from flask import Flask, render_template
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict

class FlaskWithHamlish(Flask):
	jinja_options = ImmutableDict(
		extensions=[HamlishExtension]
	)
app = FlaskWithHamlish(__name__)

@app.route('/')
def hello_world():
	return render_template('index.haml', username="John")