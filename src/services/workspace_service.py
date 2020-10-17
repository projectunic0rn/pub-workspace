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
    def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """abstract method to create workspace channel"""

    @abstractmethod
    def set_channel_topic(self, channel_topic, workspace_entity):
        """abstract method to create workspace channel"""

    @abstractmethod
    def post_message(self, message, workspace_entity):
        """abstract method to create workspace channel"""

    @abstractmethod
    def get_username(self, auth_token, user_id=None):
        """abstract method to create workspace channel"""

