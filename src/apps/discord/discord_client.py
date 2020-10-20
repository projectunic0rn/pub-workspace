"""Discord client to handle incoming events from workspace.
   Docs https://discordpy.readthedocs.io/en/latest/api.html
"""
import os
import discord
from src.shared_core.entry import Entry
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.services.slack_workspace_service import SlackWorkspaceService
from src.init_logger import InitLogger
from src.apps.const import APP_VERSION, DISCORD_WORKSPACE, SLACK_WORKSPACE

logger = InitLogger.instance(DISCORD_WORKSPACE, os.environ["APP_ENV"])
workspace_services = {SLACK_WORKSPACE: SlackWorkspaceService(
), DISCORD_WORKSPACE: DiscordWorkspaceService()}
entry = Entry(workspace_services)
logger.warn(f'discord.py version: {discord.__version__}')

class DiscordEventClient(discord.Client):
    """Class to handle events from discord"""
    async def on_ready(self):
        """Override on_ready, indicates client has connected"""
        logger.warn(f'app version: {APP_VERSION}')
        logger.warn('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        """Override on_message, indicates message posted to channel"""
        if message.author == self.user:
            return

        author = f'{message.author.name}#{message.author.discriminator}'
        await entry.process_message_posted_event(
            message.content,
            message.channel.id,
            author,
            DISCORD_WORKSPACE)
        logger.info('Message from {0.author}: {0.content}'.format(message))


client = DiscordEventClient()
client.run(os.environ['DISCORD_BOT_TOKEN'])
