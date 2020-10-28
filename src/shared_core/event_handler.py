# pylint: disable=line-too-long
"""Handle events from all apps independent of app
   workspace type e.g. slack, discord, etc.
"""
import os
from sqlalchemy.orm import Session
from src.persistence.workspace_entity import WorkspaceEntity
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_message import WorkspaceMessage
from src.shared_core.message_to_markdown import MessageToMarkdown
from src.services.pub_service import PubService
from src.init_logger import InitLogger
from src.utils.patch_ops import patch_replace_op


class EventHandler:  # pylint: disable=too-few-public-methods
    """EventHandler reacts to events of interest
       for all workspace apps e.g. app install, message posted
    """

    def __init__(self, workspace_services: [str, WorkspaceService]):
        self.workspace_services = workspace_services
        self.app_url = os.environ['APP_URL']
        self.pub_service = PubService()
        self.logger = InitLogger.instance()

    async def on_app_install(self, workspace_entity: WorkspaceEntity):
        """Manage app installs, create channel, set topic, persist
           workspace data"""
        # Consider establishing session as part of events/requests received
        session = Session()
        await self.join_channels(workspace_entity)
        await self.create_channel(workspace_entity)
        await self.link_project(workspace_entity)
        session.add(workspace_entity)
        session.commit()
        session.close()

    async def on_message_posted(self, workspace_message: WorkspaceMessage, session: Session):
        """Manage message posts, transform message, query all workspaces,
           distribute messages to all workspaces."""
        # Move message_to_markdown logic when we start sending
        # messages to other channels
        self.logger.debug(f"in {self.on_message_posted.__name__}")
        message_to_markdown = MessageToMarkdown(workspace_message.message)
        message_to_markdown.add_quote_block().add_author_signature(
            workspace_message.author, workspace_message.workspace_type)
        message = message_to_markdown.message

        workspace_channel_id = workspace_message.channel_id
        workspaces = session.query(WorkspaceEntity).all()
        string_workspace_channel_id = str(workspace_channel_id)
        for workspace in workspaces:
            if workspace.generated_channel_id == string_workspace_channel_id:
                continue
            workspace_service = self.workspace_services[workspace.workspace_type]
            await workspace_service.post_message(message, workspace)

    async def join_channels(self, workspace):
        """Generate dev questions channel"""
        workspace_service = self.workspace_services[workspace.workspace_type]
        await workspace_service.join_all_channels(workspace)

    async def create_channel(self, workspace_entity):
        """Generate dev questions channel"""
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        workspace_entity.generated_channel_name = 'dev-questions'
        try:
            channel = await workspace_service.create_channel(workspace_entity)
        except:
            self.logger.critical(
                f'failed to create {workspace_entity.generated_channel_name} channel')
            raise
        workspace_entity.generated_channel_id = channel.id
        workspace_entity.generated_channel_name = channel.name
        await workspace_service.set_channel_topic(f'Channel for sending cross-platform messages across all workspaces for projects posted on {self.app_url}/projects.\n Use this channel to ask for help or find collaborators on a challenge you\'re facing.', workspace_entity)

    async def link_project(self, workspace_entity):
        """Associate workspace to project"""
        project = self.pub_service.get_project(workspace_entity.project_id)
        patch_operations = []
        patch_operations.append(patch_replace_op(
            '/workspaceAppInstalled', True))
        patch_operations.append(patch_replace_op(
            '/workspaceId', workspace_entity.workspace_id))

        workspace_entity.username = self.fetch_username(workspace_entity)
        patch_operations.append(patch_replace_op(
            '/workspaceMemberName', workspace_entity.username))

        workspace_entity.project_channel_id = await self.fetch_project_channel_id(
            workspace_entity, project['communicationPlatformUrl'])
        patch_operations.append(patch_replace_op(
            '/workspaceProjectChannelId', workspace_entity.project_channel_id))

        workspace_entity.project_channel_name = await self.fetch_project_channel_name(
            workspace_entity)
        patch_operations.append(patch_replace_op(
            '/workspaceProjectChannelName', workspace_entity.project_channel_name))

        workspace_entity.project_channel_recent_messages = "\t".join(await self.fetch_project_channel_messages(workspace_entity))
        patch_operations.append(patch_replace_op(
            '/workspaceRecentMessages', workspace_entity.project_channel_recent_messages))

        self.pub_service.patch_project(project['id'], patch_operations)

    def fetch_username(self, workspace_entity):
        """Get the username if it isn't already present
           on workspace entity
        """
        if workspace_entity.username != "":
            return workspace_entity.username
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        return workspace_service.get_username(workspace_entity.auth_token)

    async def fetch_project_channel_id(self, workspace_entity, invite_url):
        """Get the id of the primary project channel"""
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        return await workspace_service.select_project_channel_id(workspace_entity, invite_url=invite_url)

    async def fetch_project_channel_name(self, workspace_entity):
        """Get the id of the primary project channel"""
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        return await workspace_service.get_project_channel_name(workspace_entity)

    async def fetch_project_channel_messages(self, workspace_entity):
        """Get the id of the primary project channel"""
        workspace_service = self.workspace_services[workspace_entity.workspace_type]
        return await workspace_service.get_project_recent_messages(workspace_entity)
