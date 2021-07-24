from flask import Flask
from geocalc import geocalc

app = Flask(__name__)
app.register_blueprint(geocalc, url_prefix='')


@app.route("/")
def index():
    return "Original page"
