#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route("/status")
def app_status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def cool_stats():
    return jsonify({
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"),
        "places": storage.count("places"),
        "reviews": storage.count("reviews"),
        "states": storage.count("states"),
        "users": storage.count("users")
    })
