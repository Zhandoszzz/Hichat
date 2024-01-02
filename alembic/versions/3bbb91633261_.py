"""empty message

Revision ID: 3bbb91633261
Revises: a0c4b7a4a99b
Create Date: 2024-01-02 16:23:06.561486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bbb91633261'
down_revision: Union[str, None] = 'a0c4b7a4a99b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()')))
    op.add_column('users', sa.Column('image_path', sa.String()))
    op.add_column('users', sa.Column('username', sa.String(), nullable=False, unique=True))
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'image_path')
    op.drop_column('users', 'username')
    op.drop_column('users', 'password')
