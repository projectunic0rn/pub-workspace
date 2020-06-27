from slack import WebClient
from slack.errors import SlackApiError
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity

class SlackWorkspaceService(WorkspaceService):
    def __init__(self, token=""):
        self.client = WebClient(token=token)

    def set_client_token(self, token):
        self.client.token = token
    
    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        self.set_client_token(workspace_entity.auth_token)
        try:
            response = self.client.conversations_create(name=workspace_entity.generated_channel_name)
        except SlackApiError as e:
            # ignore bot message 
            print(f"slack request failed and raised: {e.response['error']}")
        return WorkspaceChannel(response['channel']['id'], response['channel']['name'])
    
    async def set_channel_topic(self, channel_topic, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        self.client.conversations_setTopic(channel=workspace_entity.generated_channel_id, topic=channel_topic)

    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        self.client.chat_postMessage(channel=workspace_entity.generated_channel_id, text=message)

    def get_user_info(self, user_id, workspace_entity: WorkspaceEntity):
        self.set_client_token(workspace_entity.auth_token)
        user_info = self.client.users_info(user=user_id)
        return user_info
