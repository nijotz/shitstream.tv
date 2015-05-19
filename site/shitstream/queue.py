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
    curs = conn.cursor()
    curs.execute('LISTEN queue;')

    epoll = select.epoll()
    epoll.register(conn, select.EPOLLIN)

    while True:
        events = epoll.poll()
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            emit('change', {'msg': 'Change'})
