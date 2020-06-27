import discord
import os
from src.services.workspace_service import WorkspaceService
from src.shared_core.data_objects.workspace_channel import WorkspaceChannel
from src.persistence.workspace_entity import WorkspaceEntity

class DiscordWorkspaceService(WorkspaceService):
    def __init__(self):
        self.client = discord.Client()
    
    async def get_guild(self, workspace_id):
        guild = await self.client.fetch_guild(workspace_id)
        return guild
    
    async def get_channel(self, channel_id):
        channel = await self.client.fetch_channel(channel_id)
        return channel

    async def create_channel(self, workspace_entity: WorkspaceEntity) -> WorkspaceChannel:
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=True)
        print('in discord create_channel')
        guild = await self.get_guild(workspace_entity.workspace_id)
        channel = await guild.create_text_channel(workspace_entity.generated_channel_name)
        if channel is None:
            # TODO: Test scenario if channl is deleted
            # TODO: Test Scenario if premissions are granted
            # TODO: Test scenario if channel is renamed
            # TODO: Test scenario if channel is removed
            # TODO Raise and log error if trouble creating channel
            pass
        print('complete in discord create_channel')
        await self.client.logout()
        return WorkspaceChannel(channel.id, channel.name)

    async def set_channel_topic(self, channel_topic, workspace_entity: WorkspaceEntity):
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=True)
        channel = await self.get_channel(workspace_entity.generated_channel_id)
        await self.client.logout()
        await channel.edit(topic=channel_topic)
    
    async def post_message(self, message, workspace_entity: WorkspaceEntity):
        await self.client.login(os.environ['DISCORD_BOT_TOKEN'], bot=True)
        channel = await self.get_channel(workspace_entity.generated_channel_id)
        await channel.send(content=message)
        await self.client.logout()
