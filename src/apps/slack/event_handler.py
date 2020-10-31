# pylint: disable=line-too-long
"""receive and forward slack events"""
import asyncio
from sqlalchemy.orm import Session
from src.persistence.workspace_entity import WorkspaceEntity
from src.shared_core.entry import Entry
from src.services.slack_workspace_service import SlackWorkspaceService
from src.services.discord_workspace_service import DiscordWorkspaceService
from src.apps.const import SLACK_WORKSPACE, DISCORD_WORKSPACE

workspace_services = {SLACK_WORKSPACE: SlackWorkspaceService(
), DISCORD_WORKSPACE: DiscordWorkspaceService()}
entry = Entry(workspace_services)

def resolve_event(event_data):
    """resolve and process event types - currently
       only handles posted messages and app install
    """
    # handle message type event
    if event_data["event"]["type"] == "message":
        handle_message_event(event_data)


def handle_message_event(event_data):
    """process new message posted to slack channel"""
    try:
        # ignore event if posted by bot
        if event_data["event"]["bot_id"]:
            return
    except KeyError:
        # fall through
        pass

    try:
        # skip message event if subtype is present
        if event_data["event"]["subtype"]:
            return
    except KeyError:
        # fall through
        pass

    # Potential performance improvement here - we're making an
    # api request for the slack username each time a message
    # is posted since it is not available from the event data
    session = Session()
    workspace = session.query(WorkspaceEntity).filter(
        WorkspaceEntity.generated_channel_id == event_data['event']['channel']).first()
    session.close()
    if workspace is None:
        return
    slack_workspace_service = workspace_services[SLACK_WORKSPACE]
    user_display_name = slack_workspace_service.get_username(
        workspace.auth_token, event_data['event']['user'])
    asyncio.run(
        entry.process_message_posted_event(
            event_data['event']['text'],
            event_data['event']['channel'],
            user_display_name,
            SLACK_WORKSPACE))
