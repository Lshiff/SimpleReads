"""Add library to UBC

Revision ID: dcfc6ba15b68
Revises: cb1c9a068605
Create Date: 2023-12-20 01:41:54.673453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcfc6ba15b68'
down_revision = 'cb1c9a068605'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_book_connections', schema=None) as batch_op:
        batch_op.add_column(sa.Column('library', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_book_connections', schema=None) as batch_op:
        batch_op.drop_column('library')

    # ### end Alembic commands ###
