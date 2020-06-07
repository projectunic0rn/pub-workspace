"""Entry point for flask app."""
import time
from flask import request, Flask, abort
from request_validator import RequestValidator

app = Flask(__name__)

@app.route("/events", methods=["POST"])
def events():
    """route for slack events"""
    request_validator = RequestValidator()
    headers = request.headers
    data = request.get_data()
    if request_validator.is_valid(headers, data, time.time()):
        event_data = request.get_json()
        if event_data["type"] == "url_verification":
            return event_data["challenge"]
        return event_data["token"] # process event here
    return abort(400)
