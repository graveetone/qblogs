"""empty message

Revision ID: 072b875395a9
Revises: 6eab27628f17
Create Date: 2021-12-02 00:07:22.075984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '072b875395a9'
down_revision = '6eab27628f17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_tags_ibfk_2', 'post_tags', type_='foreignkey')
    op.drop_constraint('post_tags_ibfk_1', 'post_tags', type_='foreignkey')
    op.create_foreign_key(None, 'post_tags', 'post', ['post_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'post_tags', 'tag', ['tag_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post_tags', type_='foreignkey')
    op.drop_constraint(None, 'post_tags', type_='foreignkey')
    op.create_foreign_key('post_tags_ibfk_1', 'post_tags', 'post', ['post_id'], ['id'])
    op.create_foreign_key('post_tags_ibfk_2', 'post_tags', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###
