"""add xp_multiplier and update status default

Revision ID: 5b2e83cd9f1a
Revises: 3a7f92bc1d4e
Create Date: 2026-06-14 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision = '5b2e83cd9f1a'
down_revision = '3a7f92bc1d4e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('rooms', sa.Column('xp_multiplier', sa.Float(), nullable=True))
    op.execute("UPDATE rooms SET xp_multiplier = 1.3 WHERE xp_multiplier IS NULL")
    op.alter_column('rooms', 'xp_multiplier', nullable=False)

def downgrade() -> None:
    op.drop_column('rooms', 'xp_multiplier')