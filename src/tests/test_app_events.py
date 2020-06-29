# TODO: Test scenario if channl is deleted
# TODO: Test Scenario if premissions arent granted, what do i do here? 
# TODO: Test scenario if channel is renamed
# TODO: Test scenario if channel is removed
# TODO: Test channel is created for each workspace
"""Validate slack request"""
import hashlib
import hmac
import os
import slack
import discord
import asyncio
import pytest
from src.services.slack_workspace_service import SlackWorkspaceService
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.shared_core.entry import Entry

class TestAppEvents: # pylint: disable=too-few-public-methods
    """RequestValidator contains a single method that
       validates the slack request
    """
    @pytest.mark.skip
    def test_slack_channel_created_on_install(self):
        # Arrange
        workspace_services = {'slack': SlackWorkspaceService(), 'discord': DiscordWorkspaceService()}
        slack_auth_token = 'xoxb-592647108848-1198713281185-WzWODm2xS2JPMb5wHMMO9wqe' # os.environ['SLACK_TEST_AUTH_TOKEN']
        generated_channel_present = False
        slack_client = slack.WebClient(slack_auth_token)
        entry = Entry(workspace_services)
        # Act
        asyncio.run(entry.process_app_installed_event('slack', 'THEK136QY', 'Project Unicorn Test', slack_auth_token))
        # Assert
        response = slack_client.conversations_list()
        channels = response['channels']
        for channel in channels:
            if channel['name'] == 'dev-questions':
                generated_channel_present = True
        assert generated_channel_present == True
