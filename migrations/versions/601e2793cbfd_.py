"""empty message

Revision ID: 601e2793cbfd
Revises: 8380bd849f7d
Create Date: 2022-11-25 20:02:13.036914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '601e2793cbfd'
down_revision = '8380bd849f7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=75), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('tweet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tweet_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet')
    # ### end Alembic commands ###
