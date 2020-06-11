"""Entry point for discord flask app."""
import os
from flask import Flask
from discord_client import DiscordClient

def create_app():
    """Startuo method to initialize flask and
       connect discord client.
    """
    flask_app = Flask(__name__)
    client = DiscordClient()
    client.run(os.environ['DISCORD_BOT_TOKEN'])
    return flask_app

app = create_app()

@app.route('/')
def index():
    """placeholder route - to be removed"""
    return 'Pub discord workspace bot!'
