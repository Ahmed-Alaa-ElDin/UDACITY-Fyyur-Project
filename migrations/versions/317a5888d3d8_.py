"""empty message

Revision ID: 317a5888d3d8
Revises: 7b55b762dd9a
Create Date: 2020-09-19 00:31:01.641357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '317a5888d3d8'
down_revision = '7b55b762dd9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id')
    )
    # op.add_column('artist', sa.Column('genre', sa.String(), nullable=True))
    # op.add_column('venue', sa.Column('genre', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genre')
    op.drop_column('artist', 'genre')
    op.create_table('gen_ven',
    sa.Column('genres_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['genres_id'], ['genres.id'], name='gen_ven_genres_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='gen_ven_venue_id_fkey'),
    sa.PrimaryKeyConstraint('genres_id', 'venue_id', name='gen_ven_pkey')
    )
    op.create_table('gen_art',
    sa.Column('genres_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='gen_art_artist_id_fkey'),
    sa.ForeignKeyConstraint(['genres_id'], ['genres.id'], name='gen_art_genres_id_fkey'),
    sa.PrimaryKeyConstraint('genres_id', 'artist_id', name='gen_art_pkey')
    )
    op.create_table('shows',
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='shows_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='shows_venue_id_fkey'),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id', name='shows_pkey')
    )
    op.create_table('genres',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='genres_pkey')
    )
    op.drop_table('show')
    # ### end Alembic commands ###
