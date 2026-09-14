"""add last few columns to posts table

Revision ID: 48e818c7797d
Revises: 4674ec2892b8
Create Date: 2026-09-14 17:32:24.187046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e818c7797d'
down_revision: Union[str, Sequence[str], None] = '4674ec2892b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add published and created_at to posts, matching models.Post
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('now()'),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Undo upgrade(): remove both columns
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
