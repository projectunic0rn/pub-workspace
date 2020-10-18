"""Module to make http requests to external services"""
import requests
from src.init_logger import InitLogger


class HttpClient:
    """Defines standard http methods to make
       network requests
    """

    def __init__(self):
        self.logger = InitLogger.instance()

    def get(self, endpoint, headers=None):
        """http get method"""
        response = requests.get(endpoint, headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            self.logger.critical(error.response)
            raise error

    def put(self, endpoint, headers=None, data=None, body=None):
        """http put method"""
        response = requests.put(endpoint, data=data, json=body,
                                headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            self.logger.critical(error.response)
            raise error

    def post(self, endpoint, headers=None, data=None, body=None):
        """http post method"""
        response = requests.post(endpoint, data=data, json=body,
                                 headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            self.logger.critical(error.response)
            raise error
