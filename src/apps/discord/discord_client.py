"""Discord client to handle incoming events from workspace.
   Docs https://discordpy.readthedocs.io/en/latest/api.html
"""
import os
import discord
import asyncio
import threading
# from src.shared_core.entry import Entry

# Consider exposing this bot install URL via http endpoint
# prod: https://discord.com/api/oauth2/authorize?client_id=552733792188497921&permissions=3152&scope=bot
# test: https://discord.com/api/oauth2/authorize?client_id=717379714456617032&permissions=3152&scope=bot
# Permissions
# Manage channels, View channels, Send messages, Add reactions
client = discord.Client()

@client.event
async def on_ready():
    """Override on_ready, indicates client has connected to discord service"""
    print('Logged on as {0}!'.format(client.user.name))

@client.event
async def on_message(message):
    """Override on_message, indicates new message posted"""
    print('Message from {0.author}: {0.content}'.format(message))

@client.event
async def on_guild_join(guild):
    """Override on_guild_join, indicates bot installed to new server"""
    # add log
    # workspace = map_guild_to_workspace_object()
    # entry = process_app_installed_event(workspace)
    # await Entry().process_app_installed_event('discord', guild.id, guild.name)
    await guild.create_text_channel('name')
    print('Guild join {0.name}'.format(guild))

async def start():
    await client.start(os.environ['DISCORD_BOT_TOKEN']) # use client.start instead of client.run

def loop_run(loop):
    loop.run_forever()

def init_discord_client_on_thread():
    loop = asyncio.get_event_loop()
    loop.create_task(start())

    thread = threading.Thread(target=loop_run, args=(loop,))
    thread.start()
