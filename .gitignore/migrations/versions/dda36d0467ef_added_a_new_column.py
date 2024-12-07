"""Added a new column

Revision ID: dda36d0467ef
Revises: 6e26bc39151a
Create Date: 2024-12-05 10:20:44.630505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dda36d0467ef'
down_revision = '6e26bc39151a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('song_recommendations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('song_name', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('song_recommendations', schema=None) as batch_op:
        batch_op.drop_column('song_name')

    # ### end Alembic commands ###
