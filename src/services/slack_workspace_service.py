# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
"""Module for making slack api calls"""
from datetime import datetime, timedelta
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

    async def join_all_channels(self, workspace):
        """Join all slack channel"""
        self.set_client_token(workspace.auth_token)
        try:
            channels = self.fetch_all_channels()
            for channel in channels:
                self.join_channel(channel['id'])
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.join_all_channels.__name__} request failed for workspace {workspace.id} and raised error: {error.response['error']}")
        return

    async def create_channel_if_not_exists(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """Create a channel on the slack workspace"""
        self.set_client_token(workspace_entity.auth_token)
        channel_id = ''
        channel_name = ''
        try:
            response = self.client.conversations_create(
                name=workspace_entity.generated_channel_name)
        except SlackApiError as error:
            if error.response['error'] == "name_taken":
                self.logger.warning(
                    f"slack {self.create_channel_if_not_exists.__name__} request failed and raised error: {error.response['error']}")
                self.logger.warning("attempting to fetch channel")
                channels = self.fetch_all_channels()
                for channel in channels:
                    if channel['name'] == workspace_entity.generated_channel_name:
                        channel = self.fetch_channel(channel=channel['id'])
                        channel_id = channel['id']
                        channel_name = channel['name']
            else:
                self.logger.critical(
                    f"slack {self.create_channel_if_not_exists.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
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
            self.logger.warning(
                f"slack {self.set_channel_topic.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
            self.logger.warning(
                "skipping setting channel topic and resuming as normal")
        return

    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        """Post message to slack channel"""
        self.set_client_token(workspace_entity.auth_token)
        try:
            self.client.chat_postMessage(
                channel=workspace_entity.generated_channel_id,
                text=message)
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.post_message.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.response['error']}")
            self.logger.warning("skipping message send and resuming as normal")
        return

    async def select_project_channel_id(self, workspace, **kwargs):
        """Select a project channel id favoring
           channel that has been most frequently
           used in given time period.
        """
        self.set_client_token(workspace.auth_token)
        try:
            channels = self.fetch_all_channels()
            project_channel_id = self.select_channel(channels)
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.select_project_channel_id.__name__} request failed for workspace {workspace.id} and raised error: {error.response['error']}")
        return project_channel_id

    async def get_project_channel_name(self, workspace):
        """Get project channel name given channel
           id
        """
        self.set_client_token(workspace.auth_token)
        try:
            channel = self.fetch_channel(workspace.project_channel_id)
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.get_project_channel_name.__name__} request failed for workspace {workspace.id} and raised error: {error.response['error']}")
        return channel['name']

    async def get_project_recent_messages(self, workspace):
        """Return number_of_messages from a channel
           given the channel id
        """
        self.set_client_token(workspace.auth_token)
        messages = []
        try:
            response = self.client.conversations_history(
                channel=workspace.project_channel_id, limit=5)
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.get_project_recent_messages.__name__} request failed for workspace {workspace.id} and raised error: {error.response['error']}")
        for message in response['messages']:
            messages.append(message['text'])
        return messages

    def fetch_all_channels(self):
        """fetch all slack channel"""
        try:
            response = self.client.conversations_list()
            channels = response['channels']
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.fetch_all_channels.__name__} request failed and raised error: {error.response['error']}")
        return channels

    def fetch_channel(self, channel):
        """Fetch slack channel"""
        try:
            response = self.client.conversations_info(channel=channel)
            channel = response['channel']
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.fetch_channel.__name__} request failed and raised error: {error.response['error']}")
        return channel

    def join_channel(self, channel):
        """Join single slack channel"""
        try:
            self.client.conversations_join(channel=channel)
        except SlackApiError as error:
            self.logger.warning(
                f"slack {self.join_channel.__name__} request failed and raised error: {error.response['error']}")

    def get_username(self, auth_token, user_id=None):
        """Get display name of slack user"""
        self.set_client_token(auth_token)
        display_name = user_id
        try:
            user_info = self.client.users_info(user=user_id)
        except SlackApiError as error:
            # fallback on user_id as display name
            self.logger.warning(
                f"slack {self.get_username.__name__} request failed, and raised error: {error.response['error']}. Falling back to user_id as author")
            return display_name
        else:
            return user_info['user']['profile']['display_name']

    def select_channel(self, channels):
        """Select project channel based on channel
           with most recent messages
        """
        max_messages = -1
        max_messages_channel = ''
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        for channel in channels:
            channel_id = channel['id']
            try:
                channel_history_latest = self.client.conversations_history(
                    channel=channel_id)
                channel_history_month = self.client.conversations_history(
                    channel=channel_id, latest=one_month_ago.timestamp())

                latest_messages_count = valid_messages_count(
                    channel_history_latest['messages'])
                month_messages_count = valid_messages_count(
                    channel_history_month['messages'])
            except SlackApiError as error:
                self.logger.warning(
                    f"slack {self.select_channel.__name__} request failed and raised error: {error.response['error']}")
            messages_diff = latest_messages_count - month_messages_count
            if messages_diff > max_messages:
                max_messages = messages_diff
                max_messages_channel = channel_id
        return max_messages_channel


def valid_messages_count(messages):
    """Count only user messages"""
    messages_count = 0
    for message in messages:
        if 'subtype' in message:
            continue
        messages_count += 1
    return messages_count
