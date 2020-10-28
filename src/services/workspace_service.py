"""Module that defines contract for workspace services"""
from abc import ABC, abstractmethod
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity


class WorkspaceService(ABC):
    """Class that defines contract for workspace services.
       Each workspace will implement this class and
       override its abstract methods
    """
    @abstractmethod
    def join_all_channels(self, workspace: WorkspaceEntity):
        """abstract method to join workspace channels"""

    @abstractmethod
    def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """abstract method to create workspace channel"""

    @abstractmethod
    def set_channel_topic(self, channel_topic, workspace_entity):
        """abstract method to set workspace channel topic"""

    @abstractmethod
    def post_message(self, message, workspace_entity):
        """abstract method to post message to workspace channel"""

    @abstractmethod
    def get_username(self, auth_token, user_id=None):
        """abstract method to get username"""

    @abstractmethod
    def select_project_channel_id(self, workspace, **kwargs):
        """Select a project channel id"""

    @abstractmethod
    def get_project_channel_name(self, workspace):
        """Get project channel name given channel
           id
        """

    @abstractmethod
    def get_project_recent_messages(self, workspace):
        """Return number_of_messages from a channel
           given the channel id
        """
