"""empty message

Revision ID: b3ae32b28f07
Revises: 027998395c2e
Create Date: 2020-05-14 00:48:57.300930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3ae32b28f07'
down_revision = '027998395c2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items_labels',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('label_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('item_id', 'label_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items_labels')
    # ### end Alembic commands ###
