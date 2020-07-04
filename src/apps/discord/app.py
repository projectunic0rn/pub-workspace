# pylint: disable=line-too-long
"""Entry point for discord flask app."""
import os
from flask import Flask, Response
from src.apps.discord.discord_client import init_discord_client_on_thread

def create_app():
    """Startup method to initialize flask and
       connect discord client.
    """
    flask_app = Flask(__name__)
    init_discord_client_on_thread()
    return flask_app

client_id = os.environ['DISCORD_CLIENT_ID']
app = create_app()

@app.route("/", methods=["GET"])
def root():
    """root index"""
    return Response(status="200")

@app.route("/info", methods=["GET"])
def info():
    """app info"""
    return {
        'name': 'discord',
        'version': 'v0.0.14',
        # Permissions Manage channels, View channels, Send messages, Add reactions
        'installUrl': f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=3152&scope=bot',
    }
