#!/bin/python
from flask import current_app
import os
import psycopg2
from shitstream import db
from shitstream.models import Played, Weight
import subprocess

path = os.path.dirname(os.path.realpath(__file__))


def run():
    dburi = current_app.config['SQLALCHEMY_DATABASE_URI']
    conn = psycopg2.connect(dburi)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()

    while True:
        next_video = Weight.pick()
        played = Played()
        played.video = next_video
        db.session.add(played)
        db.session.commit()
        curs.execute('NOTIFY queue;')
        subprocess.call(['ffmpeg',                         '-re',                         '-i', current_app.config['MOVIE_DIR'] + '/' + next_video.filename,                         '-c', 'copy',                         '-f', 'flv', 'rtmp://localhost:1935/stream/live'])
