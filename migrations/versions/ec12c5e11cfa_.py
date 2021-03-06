"""empty message

Revision ID: ec12c5e11cfa
Revises: 3d30e4d6facc
Create Date: 2020-05-26 00:34:05.428441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec12c5e11cfa'
down_revision = '3d30e4d6facc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
    sa.Column('user_role_id', sa.Integer(), nullable=False),
    sa.Column('user_role', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('user_role_id'),
    sa.UniqueConstraint('user_role')
    )
    op.add_column('users', sa.Column('user_role', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_role')
    op.drop_table('user_roles')
    # ### end Alembic commands ###
