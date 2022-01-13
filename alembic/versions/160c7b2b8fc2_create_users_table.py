"""create users table

Revision ID: 160c7b2b8fc2
Revises: 7525eed212a1
Create Date: 2022-01-12 12:49:24.996606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '160c7b2b8fc2'
down_revision = '7525eed212a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
