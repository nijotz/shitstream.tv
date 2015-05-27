from datetime import datetime
from random import random
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
    number = db.Column(db.Integer)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship('Video', backref=db.backref('queue',
        lazy='dynamic'))


class Played(Base):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship('Video', backref=db.backref('played',
        lazy='dynamic'))


class Video(Base):
    key = db.Column(db.Text)
    filename = db.Column(db.Text)
    origin = db.Column(db.Text)


class Weight(Base):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship('Video', backref=db.backref('weight',
        lazy='dynamic'))
    weight = db.Column(db.Integer)

    def pick(self):
        entries = self.query.all()
        total_weight = sum(map(lambda entry: entry.weight, entries))
        choice_weight = total_weight*random()
        chosen = None
        i = 0

        while choice_weight > 0:
            chosen = entries[i]
            choice_weight -= chosen.weight
            i += 1

        chosen.weight //= 10

        for entry in entries:
            entry.weight += 1

        db.session.add_all(entries)
        db.session.commit()

        return chosen.video
