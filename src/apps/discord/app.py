# pylint: disable=line-too-long
"""Entry point for discord flask app."""
import os
from flask import Flask, Response
from src.apps.version import APP_VERSION

client_id = os.environ['DISCORD_CLIENT_ID']
app = Flask(__name__)

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
        'installUrl': f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=3152&scope=bot',
    }
