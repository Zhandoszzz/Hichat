"""add foreign keys

Revision ID: f2d4bcfe89f4
Revises: 83d1916a8f2c
Create Date: 2024-01-02 16:57:19.911575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2d4bcfe89f4'
down_revision: Union[str, None] = '83d1916a8f2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    op.add_column('messages', sa.Column('receiver_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))


def downgrade() -> None:
    op.drop_constraint('messages_owner_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_receiver_id_fkey', 'messages', type_='foreignkey')
    op.drop_column('messages', 'owner_id')
    op.drop_column('messages', 'receiver_id')
