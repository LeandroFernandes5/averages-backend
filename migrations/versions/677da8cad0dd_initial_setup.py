"""Initial setup

Revision ID: 677da8cad0dd
Revises: 
Create Date: 2021-06-21 22:07:02.818083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677da8cad0dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('role', sa.String(length=64), server_default='Driver', nullable=False),
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.Column('password_reset_token', sa.String(length=128), nullable=True),
    sa.Column('status', sa.String(length=64), server_default='Pending', nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
