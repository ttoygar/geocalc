from flask import Flask

from .geocalc.geocalc import geocalc


def create_app():
    app = Flask(__name__)

    # from fgeocoder.geocalc.geocalc import geocalc
    app.register_blueprint(geocalc)

    return app
