# pylint: disable=line-too-long
"""Entry point for flask app."""
import os
import time
import slack
import json
from flask import request, Flask, abort, redirect, Response
from src.apps.const import APP_VERSION, SLACK_WORKSPACE
from src.apps.slack.request_validator import RequestValidator
from src.init_logger import InitLogger
from azure.servicebus import ServiceBusClient, Message

connstr = os.environ['SERVICE_BUS_CONN_STR']
queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

logger = InitLogger.instance(SLACK_WORKSPACE, os.environ["APP_ENV"])

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
redirect_uri = os.environ["SLACK_REDIRECT_URI"]
app_url = os.environ["APP_URL"]
app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    """root index"""
    return Response(status="200")

@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    """Route to handle exchange of code for auth token"""
    # Retrieve the auth code from the request params
    auth_code = request.args['code']

    # An empty string is a valid token for this request
    client = slack.WebClient(token="")

    # Request the auth tokens from Slack
    response = client.oauth_v2_access(
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code,
        redirect_uri=redirect_uri
    )

    event_data = {
        'team_id': response['team']['id'],
        'team_name': response['team']['name'],
        'access_token': response['access_token'],
        'event': {
            'type': 'app_install'
        }
    }
    queue_event(event_data)
    return redirect(f'{app_url}/oauth/?app={SLACK_WORKSPACE}')

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
        'installUrl': f'https://slack.com/oauth/v2/authorize?client_id={client_id}&scope=channels:manage,channels:join,channels:read,chat:write,chat:write.customize,reactions:read,reactions:write,users:read,channels:history&redirect_uri={redirect_uri}'
    }

def queue_event(event_data):
    data = json.dumps(event_data)
    with ServiceBusClient.from_connection_string(connstr) as client:
        with client.get_queue_sender(queue_name) as sender:
            single_message = Message(data)
            sender.send_messages(single_message)
