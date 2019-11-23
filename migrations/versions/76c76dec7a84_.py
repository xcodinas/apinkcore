"""empty message

Revision ID: 76c76dec7a84
Revises: 
Create Date: 2019-11-23 17:51:52.049093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c76dec7a84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('values_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.Column('measured_at', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('moisture', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('values_history')
    op.drop_table('user')
    # ### end Alembic commands ###
