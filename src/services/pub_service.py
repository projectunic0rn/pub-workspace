import os
from src.services.http import HttpClient
from src.services.response_objects.project import Project
"""Module that defines service class for
   making requests to the pub api
"""


class PubService:
    """Class that defines valid methods for interacting 
       with pub api
    """

    def __init__(self):
        self.pub_endpoint = os.environ['PUB_API_ENDPOINT']
        self.headers = {
            'X-Api-Key': os.environ['PUB_API_TOKEN'], 'Content-Type': 'application/json'}
        self.client = HttpClient(self.headers)

    def get_project(self, project_id) -> Project:
        """method for fetching project"""
        project = self.client.get(f'{self.pub_endpoint}/projects/{project_id}')
        return project

    def update_project(self, project):
        """method for updating project"""
        project = self.client.update(f'{self.pub_endpoint}/projects', project)
        return project
