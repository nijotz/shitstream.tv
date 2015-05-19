import select
import time

from flask import Blueprint, current_app, render_template
from flask.ext.socketio import emit
import psycopg2

from shitstream import db, socketio


mod = Blueprint('queue', __name__)

@mod.route('/')
def hello():
    return render_template('index.html')

@socketio.on('connect', namespace='/queue/')
def current():
    emit('change', {'msg': 'Connected'})

    dburi = current_app.config['SQLALCHEMY_DATABASE_URI']
    conn = psycopg2.connect(dburi)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute('LISTEN queue;')

    while True:
        if select.select([conn], [], []) == ([], [], []):
            pass
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop()
                emit('change', {'msg': 'Change'})
