# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes
"""Module for making discord api calls"""
import os
from discord import Client, HTTPException, Guild
from src.services.http import HttpClient
from src.apps.const import DISCORD_API_ENDPOINT
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity
from src.init_logger import InitLogger


class DiscordWorkspaceService(WorkspaceService):
    """Class for making discord api calls"""

    def __init__(self):
        self.client_id = os.environ['DISCORD_CLIENT_ID']
        self.client_secret = os.environ['DISCORD_CLIENT_SECRET']
        self.redirect_uri = os.environ["DISCORD_REDIRECT_URI"]
        self.client = Client()
        self.is_bot = True
        self.logger = InitLogger.instance()
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': ''}
        self.http_client = HttpClient()
        self.api_endpoint = DISCORD_API_ENDPOINT

    def get_username(self, auth_token, user_id=None):
        """Get a discord server given server id"""
        self.headers['Authorization'] = f'Bearer {auth_token}'
        user = self.http_client.get(
            f'{self.api_endpoint}/users/@me', self.headers)
        return f'{user["username"]}#{user["discriminator"]}'

    async def get_guild(self, workspace_id) -> Guild:
        """Get a discord server given server id"""
        guild = await self.client.fetch_guild(workspace_id)
        return guild

    async def get_channel(self, channel_id):
        """Get a discord channel given channel id"""
        channel = await self.client.fetch_channel(channel_id)
        return channel

    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """Create discord channel"""
        channel_name = ""
        channel_id = ""
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        try:
            guild = await self.get_guild(workspace_entity.workspace_id)
            channel = await guild.create_text_channel(workspace_entity.generated_channel_name)
        except HTTPException as error:
            self.logger.critical(
                f"failed to create channel {self.create_channel.__name__} request failed for workspace {workspace_entity.id} and channel {workspace_entity.generated_channel_name}. Error details: {error.text} (code {error.code})")
        else:
            channel_id = channel.id
            channel_name = channel.name

        self.logger.info("created discord channel")
        await self.client.logout()
        return WorkspaceChannel(channel_id, channel_name)

    async def set_channel_topic(self, channel_topic, workspace_entity: WorkspaceEntity):
        """Set discord channel topic"""
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        try:
            channel = await self.get_channel(workspace_entity.generated_channel_id)
            await channel.edit(topic=channel_topic)
        except HTTPException as error:
            self.logger.error(
                f"discord {self.set_channel_topic.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
            self.logger.error("skipping setting channel topic")
        await self.client.logout()
        self.logger.info("set discord channel topic")
        return

    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        """Post message to discord channel"""
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        try:
            channel = await self.get_channel(workspace_entity.generated_channel_id)
            await channel.send(content=message)
        except HTTPException as error:
            self.logger.warning(
                f"discord {self.post_message.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
            self.logger.warning("skipping message send and resuming as normal")
        await self.client.logout()
        self.logger.info("posted discord message")
        return

    def select_project_channel_id(self, workspace, **kwargs):
        """Get project channel id using the channel
           associated with the discord invite url.
           invite api should always be valid.
        """
        invite_code = kwargs["invite_url"].rsplit("/", 1)[1]
        invite = self.http_client.get(
            f'{self.api_endpoint}/invites/{invite_code}', self.headers)
        return invite["channel"]["id"]

    async def get_project_channel_name(self, workspace: WorkspaceEntity):
        """Get project channel name using the channel
           associated with the discord invite url.
           invite api should always be valid.
        """
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        channel_name = ""
        try:
            channel = await self.get_channel(workspace.project_channel_id)
        except HTTPException as error:
            self.logger.critical(
                f"discord {self.get_project_channel_name.__name__} request failed for workspace {workspace.id} and raised error: {error.text} (code {error.code})")
        else:
            channel_name = channel.name

        await self.client.logout()
        return channel_name

    async def get_project_recent_messages(self, workspace):
        """Return number_of_messages from a channel
           given the channel id
        """
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        messages = []
        try:
            channel = await self.get_channel(workspace.project_channel_id)
            async for message in channel.history(limit=5):
                messages.append(message.content)
        except HTTPException as error:
            self.logger.critical(
                f"discord {self.get_project_recent_messages.__name__} request failed for workspace {workspace.id} and raised error: {error.text} (code {error.code})")

        await self.client.logout()
        return messages

    def exchange_code(self, code):
        """Exchange code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'scope': 'identify'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = self.http_client.post(
            f'{self.api_endpoint}/oauth2/token', headers, data=data)
        return access_token

    def refresh_token(self, refresh_token):
        """Refresh access token once expired."""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'redirect_uri': self.redirect_uri,
            'scope': 'identify email connections'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = self.http_client.post(
            f'{self.api_endpoint}/oauth2/token', headers, data=data)
        return access_token
