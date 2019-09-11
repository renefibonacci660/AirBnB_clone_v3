#!/usr/bin/python3
""" Handles API status of our Flask instance 'app' """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_close(var=None):
    """ handles closing of app once connection is established """
    storage.close()


@app.errorhandler(404)
def not_found(var):
    """ Handles error message types when connection not completed """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or "0.0.0.0",
            port=getenv("HBNB_API_PORT") or 5000, threaded=True)
