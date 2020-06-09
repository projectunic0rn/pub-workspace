"""Entrypoint for apps into shared core module"""
class Entry:# pylint: disable=too-few-public-methods
    """Entry follows facade pattern - acts as boundary
       between apps and shared code. Includes data object
       mapping and request forwarding.
    """
    def __init__(self):
        pass

    def process_message(self):
        """Message processor, map and forward data."""
        raise NotImplementedError
