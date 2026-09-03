"""add asset_class to assets

Revision ID: f1a2b3c4d5e6
Revises: e3f5a8b2d914
Create Date: 2026-07-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f1a2b3c4d5e6'
down_revision = 'e3f5a8b2d914'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('assets', sa.Column('asset_class', sa.String(20), nullable=False, server_default='tech'))
    op.alter_column('assets', 'asset_class', server_default=None)


def downgrade():
    op.drop_column('assets', 'asset_class')
