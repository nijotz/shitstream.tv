#!/bin/python
import logging
import os
import subprocess

from flask import current_app
import psycopg2

from shitstream import db
from shitstream.models import Played, Weight


path = os.path.dirname(os.path.realpath(__file__))

def run():
    current_app.logger.setLevel(logging.DEBUG)

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

        video_file = os.path.join(current_app.config['MOVIE_DIR'], next_video.filename)
        current_app.logger.info('Playing {}'.format(video_file))
        subprocess.call(['avconv',
            '-re',
            '-v', 'warning',
            '-i', video_file,
            '-vf', 'scale=-1:480,format=yuv420p',
            '-f', 'flv',
            'rtmp://localhost:1935/stream/live'])
