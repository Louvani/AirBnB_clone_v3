#!/usr/bin/python3
'''first endpoint (route) will be to return the status of your API'''

from os import getenv

from api.v1.views import app_views
from flask import Flask, render_template, jsonify, make_response
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'

    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000

    app.run(debug=True, port=HBNB_API_PORT, host=HBNB_API_HOST, threaded=True)
