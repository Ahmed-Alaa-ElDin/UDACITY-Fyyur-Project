"""empty message

Revision ID: 02e25ac53af5
Revises: 14aaec6880dd
Create Date: 2020-09-14 20:31:25.471722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02e25ac53af5'
down_revision = '14aaec6880dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gen_art',
    sa.Column('genres_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genres_id'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('genres_id', 'artist_id')
    )
    op.create_table('gen_ven',
    sa.Column('genres_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genres_id'], ['genres.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('genres_id', 'venue_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gen_ven')
    op.drop_table('gen_art')
    # ### end Alembic commands ###
