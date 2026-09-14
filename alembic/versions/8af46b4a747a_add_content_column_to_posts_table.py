"""add content column to posts table

Revision ID: 8af46b4a747a
Revises: aa4852f520b4
Create Date: 2026-09-14 14:53:56.618486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af46b4a747a'
down_revision: Union[str, Sequence[str], None] = 'aa4852f520b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the content column to the existing posts table, matching models.Post.content
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    # Undo upgrade(): remove the content column
    op.drop_column('posts', 'content')
