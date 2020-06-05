"""Entry point for flash app."""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    """Index route for flask app"""
    return 'Pub slack workspace app!'
