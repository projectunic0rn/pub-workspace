"""Handle events from all apps independent of app 
   workspace type e.g. slack vs discord vs others
"""
import os
from sqlalchemy.orm import Session
from src.persistence.workspace_entity import WorkspaceEntity
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_message import WorkspaceMessage
from src.shared_core.message_to_markdown import MessageToMarkdown
class EventHandler: # pylint: disable=too-few-public-methods
    """EventHandler reacts to events of interest
       for all workspace apps e.g. app install, message posted
    """
    def __init__(self, workspace_services: WorkspaceService):
        self.workspace_services = workspace_services
        self.app_url = os.environ['APP_URL']

    async def on_app_install(self, workspace_entity: WorkspaceEntity):
        """Message processor, map and forward data."""
        print('in on_app_install')
        # Consider establishing session as part of events/requests received
        session = Session()
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        workspace_entity.generated_channel_name = 'dev-questions'
        channel = await workspace_service.create_channel(workspace_entity)
        workspace_entity.generated_channel_id = channel.id
        workspace_entity.generated_channel_name = channel.name
        await workspace_service.set_channel_topic(f'Dedicated channel for sending messages across all project unicorn workspaces found on {self.app_url}/projects regardless of platform (e.g. slack/discord).\nUse this channel to ask for help or find collaborators on a challenge you\'re facing.', workspace_entity)
        session.add(workspace_entity)
        session.commit()
        session.close()
        print('completed on on_app_install')
    
    async def on_message_posted(self, workspace_message: WorkspaceMessage, session: Session):
        # Move message_to_markdown logic when we start sending
        # messages outside of the generated channel 
        message_to_markdown = MessageToMarkdown(workspace_message.message)
        message_to_markdown.add_quote_block().add_author_signature(workspace_message.author, workspace_message.workspace_type)
        message = message_to_markdown.message

        workspace_channel_id = workspace_message.channel_id
        print('in on_message_posted')
        print(f'message: {message_to_markdown.message}')
        print(f'workspace: {workspace_message.channel_id}')
        workspaces = session.query(WorkspaceEntity).all()
        string_workspace_channel_id = str(workspace_channel_id)
        for workspace in workspaces:
            print(f'{workspace.generated_channel_id} == {string_workspace_channel_id}: {workspace.generated_channel_id == string_workspace_channel_id}')
            if workspace.generated_channel_id == string_workspace_channel_id:
                continue
            workspace_service = self.workspace_services[workspace.workspace_type]
            await workspace_service.post_message(message, workspace)