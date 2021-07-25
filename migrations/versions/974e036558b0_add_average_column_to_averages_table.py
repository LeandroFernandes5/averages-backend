"""Add average column to averages table

Revision ID: 974e036558b0
Revises: 5b20330c6a9d
Create Date: 2021-07-15 19:23:00.677188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '974e036558b0'
down_revision = '5b20330c6a9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('caraverages', sa.Column('average', sa.Float(precision=10, decimal_return_scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('caraverages', 'average')
    # ### end Alembic commands ###