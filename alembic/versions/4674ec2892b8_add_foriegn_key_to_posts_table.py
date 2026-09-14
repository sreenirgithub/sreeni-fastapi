"""add foriegn key to posts table

Revision ID: 4674ec2892b8
Revises: a283c29b565a
Create Date: 2026-09-14 17:24:20.221582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4674ec2892b8'
down_revision: Union[str, Sequence[str], None] = 'a283c29b565a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the owner_id column to posts, matching models.Post.owner_id
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    # Link owner_id to users.id; ON DELETE CASCADE removes a user's posts if the user is deleted
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Undo upgrade(), in reverse order: drop the foreign key, then the owner_id column
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
