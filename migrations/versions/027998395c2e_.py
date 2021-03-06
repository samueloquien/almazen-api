"""empty message

Revision ID: 027998395c2e
Revises: a93f6ef50bcd
Create Date: 2020-05-14 00:48:22.121750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '027998395c2e'
down_revision = 'a93f6ef50bcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('label_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=45), nullable=False),
    sa.Column('label_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['label_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('label_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('labels')
    # ### end Alembic commands ###
