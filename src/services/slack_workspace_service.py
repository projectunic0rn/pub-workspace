# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
"""Module for making slack api calls"""
import string
import random
from slack import WebClient
from slack.errors import SlackApiError
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity
from src.init_logger import InitLogger

class SlackWorkspaceService(WorkspaceService):
    """Class for making slack api calls implements WorkspaceService"""
    def __init__(self, token=""):
        self.client = WebClient(token=token)
        self.logger = InitLogger.instance()

    def set_client_token(self, token):
        """Set token for slack client"""
        self.client.token = token

    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """Create a channel on the slack workspace"""
        self.set_client_token(workspace_entity.auth_token)
        try:
            response = self.client.conversations_create(
                name=workspace_entity.generated_channel_name)
        except SlackApiError as error:
            if error.response['error'] == "name_taken":
                self.logger.warning(f"slack {self.create_channel.__name__} request failed and raised error: {error.response['error']}")
                self.logger.warning("attempting to rename")
                response = self.client.conversations_create(
                    name=f"{workspace_entity.generated_channel_name}-{SlackWorkspaceService.substring_generator()}")
                channel_id = response['channel']['id']
                channel_name = response['channel']['name']
            else:
                self.logger.critical(
                    f"slack {self.create_channel.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
                raise
        else:
            channel_id = response['channel']['id']
            channel_name = response['channel']['name']

        self.logger.info("created slack channel")
        return WorkspaceChannel(channel_id, channel_name)

    async def set_channel_topic(self, channel_topic, workspace_entity: WorkspaceEntity):
        """Set slack channel topic"""
        self.set_client_token(workspace_entity.auth_token)
        try:
            self.client.conversations_setTopic(
                channel=workspace_entity.generated_channel_id,
                topic=channel_topic)
        except SlackApiError as error:
            self.logger.warning(f"slack {self.set_channel_topic.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
            self.logger.warning("skipping setting channel topic and resuming as normal")
        self.logger.info("set slack channel topic")
        return

    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        """Post message to slack channel"""
        self.set_client_token(workspace_entity.auth_token)
        try:
            self.client.chat_postMessage(
                channel=workspace_entity.generated_channel_id,
                text=message)
        except SlackApiError as error:
            self.logger.warning(f"slack {self.post_message.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
            self.logger.warning("skipping message send and resuming as normal")
        self.logger.info("posted slack message")
        return

    def select_project_channel_id(self, workspace, **kwargs):
        """Select a project channel id favoring
           channel that has been most frequently
           used in given time period.
        """
        raise NotImplementedError

    def get_project_channel_name(self, workspace):
        """Get project channel name given channel
           id
        """
        raise NotImplementedError

    def get_project_recent_messages(self, workspace):
        """Return number_of_messages from a channel
           given the channel id
        """
        raise NotImplementedError

    def get_username(self, auth_token, user_id=None):
        """Get display name of slack user"""
        self.set_client_token(auth_token)
        display_name = user_id
        try:
            user_info = self.client.users_info(user=user_id)
        except SlackApiError as error:
            # fallback on user_id as display name
            self.logger.warning(f"slack {self.get_username.__name__} request failed, and raised error: {error.response['error']}. Falling back to user_id as author")
            return display_name
        else:
            return user_info['user']['profile']['display_name']

    @staticmethod
    def substring_generator(size=3, chars=string.ascii_lowercase + string.digits):
        """Generate random sequence of chars/nums"""
        return ''.join(random.choice(chars) for _ in range(size))
