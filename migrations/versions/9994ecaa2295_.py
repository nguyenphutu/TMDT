"""empty message

Revision ID: 9994ecaa2295
Revises: 0deae109ac52
Create Date: 2017-11-14 00:05:14.304549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9994ecaa2295'
down_revision = '0deae109ac52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_user_id_fkey', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'user', ['user_id'], ['id'], onupdate='cascade', ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_user_id_fkey', 'order', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
