# pylint: disable=line-too-long
"""Entry point for discord flask app."""
import os
import requests
import asyncio
from datetime import datetime, timedelta
from flask import request, Flask, Response
from flask_cors import CORS
from src.apps.const import APP_VERSION, DISCORD_WORKSPACE, SLACK_WORKSPACE
from src.services.slack_workspace_service import SlackWorkspaceService
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.shared_core.entry import Entry

client_id = os.environ['DISCORD_CLIENT_ID']
client_secret = os.environ['DISCORD_CLIENT_SECRET']
redirect_uri = os.environ["DISCORD_REDIRECT_URI"]
workspace_services = {SLACK_WORKSPACE: SlackWorkspaceService(
), DISCORD_WORKSPACE: DiscordWorkspaceService()}
entry = Entry(workspace_services)
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def root():
    """root index"""
    return Response(status="200")


@app.route("/info", methods=["GET"])
def info():
    """app info"""
    return {
        'name': 'discord',
        'version': APP_VERSION,
        # Permissions Manage channels, View channels, Send messages, Add reactions
        'installUrl': f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=3152&scope=bot%20identify&redirect_uri={redirect_uri}&response_type=code',
    }


@app.route("/finish_auth", methods=["POST"])
def post_install():
    workspace_service = workspace_services[DISCORD_WORKSPACE]
    """finalize installation of discord app"""
    auth_code = request.args['code']
    project_id = request.args['project']
    workspace_id = request.args['workspace']
    permissions = request.args['permissions']
    result = workspace_service.exchange_code(auth_code)
    access_token = result['access_token']
    refresh_token = result['refresh_token']
    token_type = result['token_type']
    scope = result['scope']

    token_expiration_date = datetime.utcnow(
    ) + timedelta(seconds=result['expires_in'])

    asyncio.run(entry.process_app_installed_event(
        DISCORD_WORKSPACE,
        workspace_id,
        "",
        project_id,
        access_token,
        refresh_token,
        token_type,
        permissions,
        scope,
        token_expiration_date))

    return Response(status="200")
