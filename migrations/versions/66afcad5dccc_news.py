"""news

Revision ID: 66afcad5dccc
Revises: e88d779424c0
Create Date: 2018-12-21 02:57:22.524606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66afcad5dccc'
down_revision = 'e88d779424c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=48), nullable=True),
    sa.Column('body', sa.String(length=720), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_news_timestamp'), 'news', ['timestamp'], unique=False)
    op.add_column('post', sa.Column('title', sa.String(length=48), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'title')
    op.drop_index(op.f('ix_news_timestamp'), table_name='news')
    op.drop_table('news')
    # ### end Alembic commands ###
