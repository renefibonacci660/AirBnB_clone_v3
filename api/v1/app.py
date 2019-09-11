#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def app_close(var=None):
    storage.close()

@app.errorhandler(404)
def not_found(var):
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or "0.0.0.0", port=getenv("HBNB_API_PORT") or 5000, threaded=True)
