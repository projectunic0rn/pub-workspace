"""Entrypoint for apps into shared core module"""
from sqlalchemy.orm import Session
from src.shared_core.event_handler import EventHandler
from src.persistence.workspace_entity import WorkspaceEntity
from src.shared_core.data_objects.workspace_message import WorkspaceMessage
from src.init_logger import InitLogger
class Entry: # pylint: disable=too-few-public-methods
    """Entry follows facade pattern - acts as boundary
       between apps and shared code. Includes data object
       mapping and request forwarding.
    """
    def __init__(self, workspace_services):
        self.event_handler = EventHandler(workspace_services)
        self.logger = InitLogger.instance()
        pass

    async def process_app_installed_event(self, workspace_type, workspace_id, workspace_name, auth_token=""):
        """Message processor, map and forward data."""
        workspace_entity = WorkspaceEntity(workspace_type=workspace_type, workspace_name=workspace_name, workspace_id=workspace_id, auth_token=auth_token)
        await self.event_handler.on_app_install(workspace_entity)
        self.logger.info('processed app installed event')
    
    def process_app_uninstalled_event(self):
        """Message processor, map and forward data."""
        # delete workspace record on app install do not delete channel from workspace
        raise NotImplementedError

    async def process_message_posted_event(self, message_content, workspace_channel_id, message_author, workspace_type):
        """Message processor, map and forward data."""
        session = Session()
        workspace = session.query(WorkspaceEntity).filter(WorkspaceEntity.generated_channel_id == workspace_channel_id).first()
        if workspace is None:
            return
        workspace_message = WorkspaceMessage(message_content, message_author, workspace_channel_id, workspace_type)
        await self.event_handler.on_message_posted(workspace_message, session)
        session.close()
        self.logger.info('processed message posted event')

    def process_message_updated_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_message_deleted_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_reaction_added_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_reaction_removed_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_channel_topic_change_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError
