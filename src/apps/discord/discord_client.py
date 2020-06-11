"""Discord client to handle incoming events from workspace.
   Docs https://discordpy.readthedocs.io/en/latest/api.html
"""
import discord
# Consider exposing this bot install URL via http endpoint
# https://discord.com/api/oauth2/authorize?client_id=552733792188497921&permissions=3152&scope=bot&guild_id=717379714456617032&disable_guild_select=true
# Permissions
# Manage channels, View channels, Send messages, Add reactions
class DiscordClient(discord.Client):
    """Class to handle overriding events of interest from discord client"""
    async def on_ready(self):
        """Override on_ready, indicates client has connected to discord service"""
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        """Override on_message, indicates new message posted"""
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_guild_join(self, guild):
        """Override on_guild_join, indicates bot installed to new server"""
        print('Guild join {0.name}'.format(guild))
