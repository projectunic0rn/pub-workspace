"""Entry point for discord flask app."""
import os
from flask import Flask
from discord_client import init_discord_client_on_thread

def create_app():
    """Startuo method to initialize flask and
       connect discord client.
    """
    flask_app = Flask(__name__)
    init_discord_client_on_thread()
    return flask_app

app = create_app()

@app.route('/')
def index():
    """placeholder route - to be removed"""
    return 'Pub discord workspace bot!'
