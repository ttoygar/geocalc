from flask import Flask

from .geocalc.geocalc import geocalc


# from fgeocoder.geocalc import geocalc
# from .geocalc import geocalc
# from fgeocoder import geocalc

def create_app():
    app = Flask(__name__)

    app.register_blueprint(geocalc)

    return app
