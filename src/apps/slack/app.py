# pylint: disable=line-too-long
"""Entry point for flask app."""
import asyncio
import os
import time
import slack
from flask import request, Flask, abort, redirect, Response
from sqlalchemy.orm import Session
from src.apps.slack.request_validator import RequestValidator
from src.shared_core.entry import Entry
from src.services.slack_workspace_service import SlackWorkspaceService
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.persistence.workspace_entity import WorkspaceEntity
from src.init_logger import InitLogger

SLACK_WORKSPACE = 'slack'
logger = InitLogger.instance(SLACK_WORKSPACE, os.environ["APP_ENV"])
logger.info(f'starting {SLACK_WORKSPACE} app')
logger.critical(f'starting {SLACK_WORKSPACE} app')

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
redirect_uri = os.environ["SLACK_REDIRECT_URI"]

app = Flask(__name__)
workspace_services = {'slack': SlackWorkspaceService(), 'discord': DiscordWorkspaceService()}
entry = Entry(workspace_services)

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

    asyncio.run(
        entry.process_app_installed_event(
            SLACK_WORKSPACE,
            response['team']['id'],
            response['team']['name'],
            response['access_token'])
        )
    return redirect(
        f'https://projectunicorn.net/oauth/?app={SLACK_WORKSPACE}')

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
            event_resolver(event_data)
            return Response(status="200")
    return abort(400)

@app.route("/info", methods=["GET"])
def info():
    """app info"""
    return {
        'name': 'slack',
        'version': 'v0.0.7',
        'install_url': f'https://slack.com/oauth/v2/authorize?client_id={client_id}&scope=channels:manage,channels:join,channels:read,chat:write,chat:write.customize,reactions:read,reactions:write,users:read&redirect_uri={redirect_uri}'
    }

def event_resolver(event_data):
    """resolve and process event types - currently
       only handles posted message
    """
    # handle message type event
    if event_data["event"]["type"] == "message":
        try:
            # ignore event if posted by bot
            if event_data["event"]["bot_id"]:
                return
        except KeyError:
            # fall through
            pass

        try:
            # skip message event if subtype is present
            if event_data["event"]["subtype"]:
                return
        except KeyError:
            # fall through
            pass

        # Potential performance improvement here - we're making an
        # api request for the slack username each time a message
        # is posted since it is not available from the event data
        session = Session()
        workspace = session.query(WorkspaceEntity).filter(
            WorkspaceEntity.generated_channel_id == event_data['event']['channel']).first()
        session.close()
        if workspace is None:
            return
        slack_workspace_service = workspace_services[SLACK_WORKSPACE]
        user_display_name = slack_workspace_service.get_user_display_name(
            event_data['event']['user'], workspace)
        asyncio.run(
            entry.process_message_posted_event(
                event_data['event']['text'],
                event_data['event']['channel'],
                user_display_name,
                SLACK_WORKSPACE))
        return
