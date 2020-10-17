# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
"""Module for making discord api calls"""
import os
import requests
from discord import Client, HTTPException
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
                        'Authorization': f''}
        self.http_client = HttpClient()
        self.api_endpoint = DISCORD_API_ENDPOINT

    def get_username(self, auth_token):
        """Get a discord server given server id"""
        self.headers['Authorization'] = f'Bearer {auth_token}'
        user = self.http_client.get(
            f'{self.api_endpoint}/users/@me', self.headers)
        return f'{user["username"]}#{user["discriminator"]}'

    async def get_guild(self, workspace_id):
        """Get a discord server given server id"""
        guild = await self.client.fetch_guild(workspace_id)
        return guild

    async def get_channel(self, channel_id):
        """Get a discord channel given channel id"""
        channel = await self.client.fetch_channel(channel_id)
        return channel

    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        """Create discord channel"""
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=self.is_bot)
        try:
            guild = await self.get_guild(workspace_entity.workspace_id)
            channel = await guild.create_text_channel(workspace_entity.generated_channel_name)
        except HTTPException as error:
            self.logger.critical(
                f"discord {self.create_channel.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
            raise error
        except:
            self.logger.critical(
                f"unexpected discord failure {self.create_channel.__name__}")
            self.logger.critical(f"inputs {workspace_entity.id}")
            raise
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

    def exchange_code(self, code):
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
