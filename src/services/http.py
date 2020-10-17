"""Module to make http requests to external services"""
import requests
import json
from src.init_logger import InitLogger


class HttpClient:
    """Defines standard http methods to make
       network requests
    """

    def __init__(self):
        self.logger = InitLogger.instance()

    def get(self, endpoint, headers={}):
        """http get method"""
        response = requests.get(endpoint, headers=headers, verify=False)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.critical(e.response)
            raise e

    def put(self, endpoint, headers={}, data={}, body={}):
        """http put method"""
        response = requests.put(endpoint, data=data, json=body,
                                headers=headers, verify=False)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.critical(e.response)
            raise e

    def post(self, endpoint, headers={}, data={}, body={}):
        """http post method"""
        response = requests.post(endpoint, data=data, json=body,
                                 headers=headers, verify=False)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.critical(e.response)
            raise e
