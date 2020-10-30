"""add unique constraint to workspace project id

Revision ID: 1c04ba5843e4
Revises: 8b02bb07cdfd
Create Date: 2020-10-30 18:01:55.034006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c04ba5843e4'
down_revision = '8b02bb07cdfd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("uq_project_id", "workspaces", ["project_id"])


def downgrade():
    op.drop_constraint("uq_project_id", "workspaces")
