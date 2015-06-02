"""merged weights and stuff

Revision ID: 53f4572295dd
Revises: ('3467248aaa71', '18922c5b115')
Create Date: 2015-05-29 06:18:19.176648

"""

# revision identifiers, used by Alembic.
revision = '53f4572295dd'
down_revision = ('3467248aaa71', '18922c5b115')

from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as BaseSession, relationship

Session = sessionmaker()

event.remove(BaseSession, 'before_commit', _SessionSignalEvents.session_signal_before_commit)
event.remove(BaseSession, 'after_commit', _SessionSignalEvents.session_signal_after_commit)
event.remove(BaseSession, 'after_rollback', _SessionSignalEvents.session_signal_after_rollback)

Base = declarative_base()


class Weight(Base):
    __tablename__ = 'weight'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.now)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('video.id'))
    video = relationship('Video', backref='weight')
    weight = sa.Column(sa.Integer)


class Video(Base):
    __tablename__ = 'video'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.now)
    key = sa.Column(sa.Text)
    filename = sa.Column(sa.Text)
    origin = sa.Column(sa.Text)


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    for video in session.query(Video):
        weight = Weight()
        weight.weight = 1
        weight.video = video
        session.add(weight)

    session.commit()

def downgrade():
    pass
