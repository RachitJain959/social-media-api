"""add user table

Revision ID: e63011493478
Revises: f1931b6ad47f
Create Date: 2025-04-11 23:47:46.354290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sat
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e63011493478'
down_revision: Union[str, None] = 'f1931b6ad47f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass

def downgrade() -> None:
    op.drop_table("users")
    pass
