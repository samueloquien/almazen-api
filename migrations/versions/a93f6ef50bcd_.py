"""empty message

Revision ID: a93f6ef50bcd
Revises: 03d66a849ce1
Create Date: 2020-05-14 00:43:33.128079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a93f6ef50bcd'
down_revision = '03d66a849ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('image_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
