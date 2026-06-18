"""add stripe fields to users

Revision ID: e3f5a8b2d914
Revises: c277764bd762
Create Date: 2026-06-03 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e3f5a8b2d914'
down_revision = 'c277764bd762'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('stripe_subscription_id', sa.String(100), nullable=True))
    op.create_unique_constraint('uq_users_stripe_customer_id', 'users', ['stripe_customer_id'])
    op.create_unique_constraint('uq_users_stripe_subscription_id', 'users', ['stripe_subscription_id'])


def downgrade():
    op.drop_constraint('uq_users_stripe_subscription_id', 'users', type_='unique')
    op.drop_constraint('uq_users_stripe_customer_id', 'users', type_='unique')
    op.drop_column('users', 'stripe_subscription_id')
    op.drop_column('users', 'stripe_customer_id')
