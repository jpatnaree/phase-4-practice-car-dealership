"""empty message

Revision ID: 3e5fd9419081
Revises: 
Create Date: 2023-12-11 21:17:10.778643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e5fd9419081'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dealership_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('owner_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(), nullable=False),
    sa.Column('date_sold', sa.Date(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealership_table.id'], name=op.f('fk_car_table_dealer_id_dealership_table')),
    sa.ForeignKeyConstraint(['owner_id'], ['owner_table.id'], name=op.f('fk_car_table_owner_id_owner_table')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car_table')
    op.drop_table('owner_table')
    op.drop_table('dealership_table')
    # ### end Alembic commands ###
