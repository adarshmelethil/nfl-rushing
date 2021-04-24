"""rushing table

Revision ID: 8af95b55be7a
Revises: 
Create Date: 2021-04-24 11:46:40.915807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af95b55be7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rushing',
    sa.Column('player', sa.String(length=64), nullable=False),
    sa.Column('team', sa.String(length=3), nullable=False),
    sa.Column('pos', sa.String(length=2), nullable=False),
    sa.Column('att', sa.Integer(), nullable=True),
    sa.Column('att_slash_g', sa.Float(), nullable=True),
    sa.Column('yds', sa.String(length=64), nullable=True),
    sa.Column('avg', sa.Float(), nullable=True),
    sa.Column('yds_slash_g', sa.Float(), nullable=True),
    sa.Column('td', sa.Integer(), nullable=True),
    sa.Column('lng', sa.String(length=32), nullable=True),
    sa.Column('first', sa.Integer(), nullable=True),
    sa.Column('first_percent', sa.Float(), nullable=True),
    sa.Column('twenty_plus', sa.Integer(), nullable=True),
    sa.Column('forty_plus', sa.Integer(), nullable=True),
    sa.Column('fum', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('player', 'team', 'pos')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rushing')
    # ### end Alembic commands ###
