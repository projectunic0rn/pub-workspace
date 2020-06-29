# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
"""Defines a shared data object for workspace channel"""
class WorkspaceChannel:
    """Defines a shared data object for workspace channel"""
    def __init__(self, channel_id, channel_name):
        self.id = channel_id
        self.name = channel_name
