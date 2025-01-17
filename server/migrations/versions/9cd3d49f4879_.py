"""empty message

Revision ID: 9cd3d49f4879
Revises: 3e5fd9419081
Create Date: 2023-12-11 22:03:51.294540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cd3d49f4879'
down_revision = '3e5fd9419081'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car_table', sa.Column('model', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car_table', 'model')
    # ### end Alembic commands ###
