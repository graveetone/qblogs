"""empty message

Revision ID: 7502df1205c7
Revises: 
Create Date: 2021-11-30 01:05:18.376457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7502df1205c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('picture_src', sa.Text(), nullable=True))
    op.add_column('post', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['author_id'], ['id'])
    op.drop_column('post_tags', 'ssd')
    op.create_unique_constraint(None, 'tag', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='unique')
    op.add_column('post_tags', sa.Column('ssd', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    op.drop_column('post', 'picture_src')
    # ### end Alembic commands ###
