"""Atleast one video

Revision ID: 70048a9e699
Revises: 53f4572295dd
Create Date: 2016-06-27 00:41:28.046500

"""

# revision identifiers, used by Alembic.
revision = '70048a9e699'
down_revision = '53f4572295dd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("insert into video (key, filename) values ('mirror', 'mirror.mp4')")
    op.execute("insert into weight (video_id, weight) values ((select id from video where key = 'mirror'), 1)")


def downgrade():
    pass
