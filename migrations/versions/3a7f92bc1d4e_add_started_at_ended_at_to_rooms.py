"""add started_at ended_at to rooms

Revision ID: 3a7f92bc1d4e
Revises: 2661ea41eb5d
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '3a7f92bc1d4e'
down_revision = '2661ea41eb5d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('rooms', sa.Column('started_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('rooms', sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True))

def downgrade() -> None:
    op.drop_column('rooms', 'ended_at')
    op.drop_column('rooms', 'started_at')