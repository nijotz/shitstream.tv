from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from shitstream import db


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Queue(Base):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship('Video', backref=db.backref('queue',
        lazy='dynamic'))

class Video(Base):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Text)
    origin = db.Column(db.Text)
