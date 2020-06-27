"""Discord client to handle incoming events from workspace.
   Docs https://discordpy.readthedocs.io/en/latest/api.html
"""
import os
import asyncio
import threading
import discord
from src.shared_core.entry import Entry
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.services.slack_workspace_service import SlackWorkspaceService
# from src.apps.contracts.app_contract import AppContract
# Manage channels, View channels, Send messages, Add reactions
client = discord.Client()
workspace_services = {'slack': SlackWorkspaceService(), 'discord': DiscordWorkspaceService()}
entry = Entry(workspace_services)
discord_bot_id = os.environ['DISCORD_BOT_ID']
discord_workspace = 'discord'

@client.event
async def on_ready():
    """Override on_ready, indicates client has connected to discord service"""
    print('Logged on as {0}!'.format(client.user.name))

@client.event
async def on_message(message):
    """Override on_message, indicates new message posted"""
    # if message is authored by bot do not re-distribute message
    if str(message.author.id) == discord_bot_id:
        return
    author = f'{message.author.name}#{message.author.discriminator}'
    await entry.process_message_posted_event(message.content, message.channel.id, author, discord_workspace)
    print('Message from {0.author}: {0.content}'.format(message))

@client.event
async def on_guild_join(guild):
    """Override on_guild_join, indicates bot installed to new server"""
    await entry.process_app_installed_event(discord_workspace, guild.id, guild.name)
    print('Guild join {0.name}'.format(guild))


def start_discord_bot():
    """start discord client"""
    client.run(os.environ['DISCORD_BOT_TOKEN'])

def loop_run(loop):
    """utility method to for event loop"""
    loop.run_forever()

def init_discord_client_on_thread():
    """get event loop and start client on thread"""
    loop = asyncio.get_event_loop()
    loop.create_task(start_discord_bot())

    thread = threading.Thread(target=loop_run, args=(loop,))
    thread.start()
