# pylint: disable=too-few-public-methods
"""Module defines objects which maps to workspaces table"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.persistence.db_config import Base


class WorkspaceEntity(Base):
    """Class defines objects which maps to workspaces table"""

    def __repr__(self):
        return f'WorkspaceEntity(id: {self.id}, \
        workspace_type: {self.workspace_type}, \
        workspace_name: {self.workspace_name}, \
        workspace_id: {self.workspace_id}, \
        generated_channel_id: {self.generated_channel_id}, \
        generated_channel_name: {self.generated_channel_name}, \
        project_id: {self.project_id}, \
        project_channel_id: {self.project_channel_id}, \
        project_channel_name: {self.project_channel_name}, \
        username: {self.username}, \
        auth_token: {self.auth_token}, \
        refresh_token: {self.refresh_token}, \
        token_type: {self.token_type}, \
        permissions: {self.permissions}, \
        token_expiration: {self.token_expiration}, \
        scope: {self.scope}, \
        created_on: {self.created_on} \
        updated_on: {self.updated_on})'

    __tablename__ = 'workspaces'

    id = Column(Integer, primary_key=True)
    workspace_type = Column(String(255))
    workspace_name = Column(String(255))
    workspace_id = Column(String(255))
    generated_channel_id = Column(String(255))
    generated_channel_name = Column(String(255))
    project_id = Column(String(255))
    project_channel_id = Column(String(255))
    project_channel_name = Column(String(255))
    project_channel_recent_messages = Column(String(255))
    username = Column(String(255), default="")
    auth_token = Column(String(255), default="")
    refresh_token = Column(String(255), default="")
    token_type = Column(String(255), default="")
    token_expiration = Column(DateTime())
    permissions = Column(String(255), default="")
    scope = Column(String(255), default="")
    created_on = Column(DateTime(), default=datetime.utcnow())
    updated_on = Column(DateTime(), default=datetime.utcnow(),
                        onupdate=datetime.utcnow())
