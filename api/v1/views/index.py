from api.v1.views import app_views
from flask import jsonify

@app_views.route("/api/v1/status")
def app_status():
    return jsonify('"status": "OK"')