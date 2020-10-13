"""Module to make http requests to external services"""
import requests


class HttpClient:
    """Class that defines several http methods and
       helper methods read and returned responses
    """

    def __init__(self, headers):
        self.headers = headers

    def get(self, endpoint):
        """http get method"""
        response = requests.get(endpoint, headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()

    def update(self, endpoint, project):
        """http update method"""
        response = requests.put(endpoint, data=project,
                                headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()
