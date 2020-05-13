"""empty message

Revision ID: 1bae017a8611
Revises: 45892c6afbcb
Create Date: 2020-05-14 01:11:33.562692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bae017a8611'
down_revision = '45892c6afbcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_prod_id', sa.Integer(), nullable=False),
    sa.Column('item_user_id', sa.Integer(), nullable=False),
    sa.Column('item_date_acquisition', sa.DateTime(timezone=3), nullable=False),
    sa.Column('item_date_expiracy', sa.DateTime(timezone=3), nullable=False),
    sa.Column('item_quantity', sa.Integer(), nullable=False),
    sa.Column('item_percent_left', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_prod_id'], ['products.prod_id'], ),
    sa.ForeignKeyConstraint(['item_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    # ### end Alembic commands ###
