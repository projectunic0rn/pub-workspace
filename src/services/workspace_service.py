from abc import ABC, abstractmethod
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity

class WorkspaceService(ABC):
    @abstractmethod
    def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        pass

    @abstractmethod
    def set_channel_topic(self, channel_topic, workspace_entity):
        pass

    @abstractmethod
    def post_message(self, message, workspace_entity):
        pass
