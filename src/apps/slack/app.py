# pylint: disable=line-too-long
"""Entry point for flask app."""
import os
import time
import json
import slack
from azure.servicebus import ServiceBusClient, Message
from flask_cors import CORS
from flask import request, Flask, abort, Response
from src.apps.const import APP_VERSION, SLACK_WORKSPACE
from src.apps.slack.request_validator import RequestValidator
from src.init_logger import InitLogger

connstr = os.environ['SERVICE_BUS_CONN_STR']
queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

logger = InitLogger.instance(SLACK_WORKSPACE, os.environ["APP_ENV"])

CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SLACK_REDIRECT_URI"]
SCOPE = 'channels:manage,channels:join,channels:read,chat:write,chat:write.customize,reactions:read,reactions:write,users:read,channels:history'
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    """root index"""
    return Response(status="200")

@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    """Route to handle exchange of code for auth token"""
    # Retrieve the auth code from the request params
    auth_code = request.args['code']
    project = request.args['project']

    # An empty string is a valid token for this request
    client = slack.WebClient(token="")

    # Request the auth tokens from Slack
    response = client.oauth_v2_access(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=auth_code,
        redirect_uri=REDIRECT_URI
    )

    event_data = {
        'team_id': response['team']['id'],
        'user_id': response['authed_user']['id'],
        'project_id': project,
        'team_name': response['team']['name'],
        'access_token': response['access_token'],
        'token_type': response['token_type'],
        'scope': response['scope'],
        'event': {
            'type': 'app_install'
        }
    }
    queue_event(event_data)
    return Response(status="200")

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
        if event_data["type"] == "event_callback":
            logger.debug(f'event_callback: {event_data}')
            queue_event(event_data)
            return Response(status="200")
    return abort(400)

@app.route("/info", methods=["GET"])
def info():
    """app info"""
    return {
        'name': 'slack',
        'version': APP_VERSION,
        'installUrl': f'https://slack.com/oauth/v2/authorize?client_id={CLIENT_ID}&scope={SCOPE}&redirect_uri={REDIRECT_URI}'
    }

def queue_event(event_data):
    """send slack event data to service bus message queue"""
    data = json.dumps(event_data)
    with ServiceBusClient.from_connection_string(connstr) as client:
        with client.get_queue_sender(queue_name) as sender:
            single_message = Message(data)
            sender.send_messages(single_message)
