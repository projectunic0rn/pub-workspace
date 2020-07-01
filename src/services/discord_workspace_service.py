# pylint: disable=invalid-overridden-method
# pylint: disable=line-too-long
"""Module for making discord api calls"""
import os
from discord import Client, HTTPException
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity
from src.init_logger import InitLogger

class DiscordWorkspaceService(WorkspaceService):
    """Class for making discord api calls"""
    def __init__(self):
        self.client = Client()
        self.is_bot = True
        self.logger = InitLogger.instance()

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
            self.logger.critical(f"discord {self.create_channel.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
            raise error
        except:
            self.logger.critical(f"unexpected discord failure {self.create_channel.__name__}")
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
            self.logger.error(f"discord {self.set_channel_topic.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
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
            self.logger.error(f"discord {self.post_message.__name__} request failed for workspace {workspace_entity.id} and raised error: {error.text} (code {error.code})")
            self.logger.error("skipping message send and resuming as normal")
        await self.client.logout()
        self.logger.info("posted discord message")
        return
