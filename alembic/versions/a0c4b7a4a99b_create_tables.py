"""create tables

Revision ID: a0c4b7a4a99b
Revises: 
Create Date: 2024-01-02 16:15:40.057789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0c4b7a4a99b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False))


def downgrade() -> None:
    op.drop_table('users')
