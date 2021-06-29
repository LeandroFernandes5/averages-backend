"""Initial setup of Car Model

Revision ID: 77dbd787cde4
Revises: 58783153e6ab
Create Date: 2021-06-30 00:44:26.975552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77dbd787cde4'
down_revision = '58783153e6ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plate', sa.String(length=64), nullable=True),
    sa.Column('brand', sa.String(length=64), nullable=True),
    sa.Column('model', sa.String(length=64), nullable=True),
    sa.Column('registerDate', sa.DateTime(), nullable=True),
    sa.Column('chassisNo', sa.String(length=64), nullable=True),
    sa.Column('obraNo', sa.String(length=64), nullable=True),
    sa.Column('inspectionDate', sa.DateTime(), nullable=True),
    sa.Column('tccExpireDate', sa.DateTime(), nullable=True),
    sa.Column('licenseDate', sa.DateTime(), nullable=True),
    sa.Column('tachographDate', sa.DateTime(), nullable=True),
    sa.Column('createdDate', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('modifiedDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cars')
    # ### end Alembic commands ###
