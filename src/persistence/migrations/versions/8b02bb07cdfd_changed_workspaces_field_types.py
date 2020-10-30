"""changed workspaces field types

Revision ID: 8b02bb07cdfd
Revises: b57ce6d1c9ca
Create Date: 2020-10-30 16:22:04.377704

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import String, Text

# revision identifiers, used by Alembic.
revision = '8b02bb07cdfd'
down_revision = 'b57ce6d1c9ca'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("workspaces", "project_channel_recent_messages", type_=Text())
    op.alter_column("workspaces", "scope", type_=Text())


def downgrade():
    op.alter_column("workspaces", "project_channel_recent_messages", type_=String(255))
    op.alter_column("workspaces", "scope", type_=String(255))
