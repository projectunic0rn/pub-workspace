from slack import WebClient
from slack.errors import SlackApiError
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity
from src.services.utility import Utility
from src.init_logger import InitLogger

class SlackWorkspaceService(WorkspaceService):
    def __init__(self, token=""):
        self.client = WebClient(token=token)
        self.logger = InitLogger.instance()

    def set_client_token(self, token):
        self.client.token = token
    
    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        self.set_client_token(workspace_entity.auth_token)
        try:
            response = self.client.conversations_create(name=workspace_entity.generated_channel_name)
        except SlackApiError as e:
            if e.response['error'] == "name_taken":
                self.logger.warning(f"slack {self.create_channel.__name__} request failed and raised error: {e.response['error']}")
                self.logger.warning(f"attempting to rename")
                response = self.client.conversations_create(name=f"{workspace_entity.generated_channel_name}-{Utility.substring_generator()}")
                channel_id = response['channel']['id']
                channel_name = response['channel']['name']
            else:
                self.logger.critical(f"slack {self.create_channel.__name__} request failed for workspace {workspace_entity.id} and raised error: {e.response['error']}")
                raise
        else:
            channel_id = response['channel']['id']
            channel_name = response['channel']['name']
        
        self.logger.info(f"created slack channel")
        return WorkspaceChannel(channel_id, channel_name)
    
    async def set_channel_topic(self, channel_topic, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        try:
            self.client.conversations_setTopic(channel=workspace_entity.generated_channel_id, topic=channel_topic)
        except SlackApiError as e:
            self.logger.warning(f"slack {self.set_channel_topic.__name__} request failed for workspace {workspace_entity.id} and raised error: {e.response['error']}")
            self.logger.warning(f"skipping setting channel topic and resuming as normal")
        self.logger.info(f"set slack channel topic")
        return

    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        try:
            self.client.chat_postMessage(channel=workspace_entity.generated_channel_id, text=message)
        except SlackApiError as e:
            self.logger.warning(f"slack {self.post_message.__name__} request failed for workspace {workspace_entity.id} and raised error: {e.response['error']}")
            self.logger.warning(f"skipping message send and resuming as normal")
        self.logger.info(f"posted slack message")
        return

    def get_user_display_name(self, user_id, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        display_name = user_id
        try:
            user_info = self.client.users_info(user=user_id)
        except SlackApiError as e:
            # fallback on user_id as display name
            self.logger.warning(f"slack {self.get_user_display_name.__name__} request failed for workspace {workspace_entity.id} and raised error: {e.response['error']}")
            self.logger.warning(f"falling back to user_id as author")
            return display_name
        else:
            return user_info['user']['profile']['display_name']
        self.logger.info(f"slack retrieved display")
        return
