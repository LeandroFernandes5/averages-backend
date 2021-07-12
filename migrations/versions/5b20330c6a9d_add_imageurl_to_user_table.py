"""Add ImageURL to User table

Revision ID: 5b20330c6a9d
Revises: 3670dbb6ee28
Create Date: 2021-07-06 21:40:45.206511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b20330c6a9d'
down_revision = '3670dbb6ee28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('imageURL', sa.String(length=128), nullable=True))
    op.drop_column('users', 'image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('users', 'imageURL')
    # ### end Alembic commands ###