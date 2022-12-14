"""empty message

Revision ID: 12305d37fad0
Revises: 072b875395a9
Create Date: 2021-12-02 06:40:43.800050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12305d37fad0'
down_revision = '072b875395a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_ibfk_1', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['author_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key('post_ibfk_1', 'post', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###
