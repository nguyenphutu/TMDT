"""empty message

Revision ID: 75b067bf4df2
Revises: b182634cc9e9
Create Date: 2017-11-13 23:12:34.793819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b067bf4df2'
down_revision = 'b182634cc9e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_user_id_fkey', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'user', ['user_id'], ['id'], ondelete='cascade')
    op.drop_constraint('order_details_order_id_fkey', 'order_details', type_='foreignkey')
    op.create_foreign_key(None, 'order_details', 'order', ['order_id'], ['id'], ondelete='cascade')
    op.drop_constraint('order_temps_user_id_fkey', 'order_temps', type_='foreignkey')
    op.create_foreign_key(None, 'order_temps', 'user', ['user_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_temps', type_='foreignkey')
    op.create_foreign_key('order_temps_user_id_fkey', 'order_temps', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'order_details', type_='foreignkey')
    op.create_foreign_key('order_details_order_id_fkey', 'order_details', 'order', ['order_id'], ['id'])
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_user_id_fkey', 'order', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###