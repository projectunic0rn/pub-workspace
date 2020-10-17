"""Module that defines service class for
   making requests to the pub api
"""
import os
from src.services.http import HttpClient


class PubService:
    """Class that defines valid methods for interacting
       with pub api
    """

    def __init__(self):
        self.pub_endpoint = os.environ['PUB_API_ENDPOINT']
        self.headers = {
            'X-Api-Key': os.environ['PUB_API_TOKEN'], 'Content-Type': 'application/json'}
        self.client = HttpClient()

    def get_project(self, project_id):
        """method for fetching project"""
        project = self.client.get(f'{self.pub_endpoint}/projects/{project_id}', self.headers)
        return project['data']

    def update_project(self, project):
        """method for updating project"""
        project = self.client.put(f'{self.pub_endpoint}/projects', self.headers, body=project)
        return project
