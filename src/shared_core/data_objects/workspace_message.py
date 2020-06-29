# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
"""Defines a shared data object for workspace message"""
class WorkspaceMessage:
    """Defines a shared data object for workspace message"""
    def __init__(self, message, author, channel_id, workspace_type):
        self.message = message
        self.author = author
        self.channel_id = channel_id
        self.workspace_type = workspace_type
