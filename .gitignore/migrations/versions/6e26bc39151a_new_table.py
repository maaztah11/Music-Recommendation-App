"""New table

Revision ID: 6e26bc39151a
Revises: 62248cfb5876
Create Date: 2024-12-05 10:18:54.087486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e26bc39151a'
down_revision = '62248cfb5876'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song_recommendations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_type', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('song_recommendations')
    # ### end Alembic commands ###
