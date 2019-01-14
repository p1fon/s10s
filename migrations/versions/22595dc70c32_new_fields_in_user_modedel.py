"""new fields in user modedel

Revision ID: 22595dc70c32
Revises: ecfa1553883d
Create Date: 2018-12-19 23:53:24.819768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22595dc70c32'
down_revision = 'ecfa1553883d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###