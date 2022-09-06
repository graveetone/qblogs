"""empty message

Revision ID: 6eab27628f17
Revises: 4f5fcbc3d726
Create Date: 2021-12-01 23:57:11.776941

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6eab27628f17'
down_revision = '4f5fcbc3d726'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=300), nullable=True),
    sa.Column('file', sa.BLOB(), nullable=True),
    sa.Column('mimetype', mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='image_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
