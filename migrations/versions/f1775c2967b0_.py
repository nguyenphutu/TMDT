"""empty message

Revision ID: f1775c2967b0
Revises: 337906bc876c
Create Date: 2017-10-19 15:02:11.355476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1775c2967b0'
down_revision = '337906bc876c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'products', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    # ### end Alembic commands ###