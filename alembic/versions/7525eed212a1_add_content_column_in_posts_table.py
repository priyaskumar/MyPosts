"""add content column in  posts table

Revision ID: 7525eed212a1
Revises: 78f2789014f8
Create Date: 2022-01-12 12:45:11.627807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7525eed212a1'
down_revision = '78f2789014f8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
