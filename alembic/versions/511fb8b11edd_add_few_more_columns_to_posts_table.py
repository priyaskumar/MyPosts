"""add few more columns to posts table

Revision ID: 511fb8b11edd
Revises: 6a2fcd14c339
Create Date: 2022-01-12 13:04:03.734162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '511fb8b11edd'
down_revision = '6a2fcd14c339'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
       
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
