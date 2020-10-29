# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes
"""Module for making discord api calls"""
import os
from datetime import datetime, timedelta
from discord import Client, HTTPException, Guild, abc, TextChannel
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

    async def join_all_channels(self, workspace):
        pass

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

    async def create_channel_if_not_exists(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """Create discord channel"""
        channel_name = ""
        channel_id = ""
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        try:
            guild = await self.get_guild(workspace_entity.workspace_id)
            channels = await guild.fetch_channels()
            channel = None
            channel_exists = False
            for chn in channels:
                if chn.name == workspace_entity.generated_channel_name:
                    channel_exists = True
                    channel = chn

            if not channel_exists:
                channel = await guild.create_text_channel(workspace_entity.generated_channel_name)
        except HTTPException as error:
            self.logger.critical(
                f"failed to create channel {self.create_channel_if_not_exists.__name__} request failed for workspace {workspace_entity.id} and channel {workspace_entity.generated_channel_name}. Error details: {error.text} (code {error.code})")
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

    async def select_project_channel_id(self, workspace: WorkspaceEntity, **kwargs):
        """Default to getting project channel id associated
           to the discord invite. If workspace id does match
           invite guild id then we fetch guild channel and
           select project channel id that belongs to workspace
        """
        channel_id = ""

        invite_code = kwargs["invite_url"].rsplit("/", 1)[1]
        invite = self.http_client.get(
            f'{self.api_endpoint}/invites/{invite_code}', self.headers)
        # invite could be invalid
        if invite['code'] == 10006:
            await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
            guild = await self.get_guild(workspace.workspace_id)
            channels = await guild.fetch_channels()
            channel_id = await self.select_channel(channels, workspace)
            await self.client.logout()
        else:
            channel_id = invite["channel"]["id"]

            # discord invite associated to project may not
            # belong to the server the app is installed on
            # so select a channel which exists on server
            if invite["guild"]["id"] != workspace.workspace_id:
                await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
                guild = await self.get_guild(workspace.workspace_id)
                channels = await guild.fetch_channels()
                channel_id = await self.select_channel(channels, workspace)
                await self.client.logout()

        return channel_id

    async def get_project_channel_name(self, workspace: WorkspaceEntity):
        """Get project channel name given project_channel_id
           using the channel associated with the discord invite url.
           invite should always be valid.
        """
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        channel_name = ""
        try:
            channel = await self.get_channel(workspace.project_channel_id)
        except HTTPException as error:
            # project channel id may result in Missing Access (code 50001)
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
                if message.author.bot:
                    continue
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

    async def select_channel(self, channels: [abc.GuildChannel], workspace: WorkspaceEntity) -> str:
        """select channel id with most message activity within
           last 30 days"""
        text_channels = []
        max_messages = -1
        max_messages_channel = ''
        for channel in channels:
            if isinstance(channel, TextChannel):
                # skip generated channel from being selected
                if channel.name == workspace.generated_channel_name:
                    continue
                text_channels.append(channel.id)

        for channel_id in text_channels:
            channel = await self.get_channel(channel_id)
            one_month_ago = datetime.utcnow() - timedelta(days=30)
            messages = await channel.history(limit=None, after=one_month_ago).flatten()
            valid_message = [m for m in messages if not m.author.bot]
            if len(valid_message) > max_messages:
                max_messages = len(valid_message)
                max_messages_channel = channel_id

        return max_messages_channel
