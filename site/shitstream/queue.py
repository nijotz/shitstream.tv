import json
import select
import time

from flask import Blueprint, current_app, render_template
from flask.ext.restful import Api, Resource
from flask.ext.socketio import emit
import psycopg2

from shitstream import db, socketio
from shitstream.models import Played, Queue


mod = Blueprint('queue', __name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


@mod.route('/')
def hello():
    return render_template('index.html')

class QueueCurrentResource(Resource):
    def get(self):
        played = Played.query.order_by(Played.created_at.desc())
        if not played: return None
        video = played.first().video
        video_json = json.loads(video.origin)
        return video_json

api.add_resource(QueueCurrentResource, '/queue/current')


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
