"""add messages table

Revision ID: 83d1916a8f2c
Revises: 3bbb91633261
Create Date: 2024-01-02 16:43:31.957776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83d1916a8f2c'
down_revision: Union[str, None] = '3bbb91633261'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('messages', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
                    sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('messages')
