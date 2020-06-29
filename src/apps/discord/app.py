"""Entry point for discord flask app."""
import os
from flask import Flask
from src.apps.discord.discord_client import init_discord_client_on_thread

def create_app():
    """Startup method to initialize flask and
       connect discord client.
    """
    flask_app = Flask(__name__)
    # TODO Fix 504 Gateway Time-out
    init_discord_client_on_thread()
    return flask_app

client_id = os.environ['DISCORD_CLIENT_ID']
app = create_app()
# install url permissons=3152 includes following
# Manage channels, View channels, Send messages, Add reactions
@app.route("/info", methods=["GET"])
def info():
    """app info"""
    return { 
        'name': 'discord',
        'version': '1.0.0',
        # TODO Consider not all permissions may be granted by users. 
        'install_url': f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=3152&scope=bot',
    }
