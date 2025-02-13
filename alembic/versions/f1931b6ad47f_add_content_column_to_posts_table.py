"""add content column to posts table

Revision ID: f1931b6ad47f
Revises: fcdde3bce8e4
Create Date: 2025-04-11 15:56:55.305292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1931b6ad47f'
down_revision: Union[str, None] = 'fcdde3bce8e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
