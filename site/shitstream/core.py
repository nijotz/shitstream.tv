from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()

def create_app(config_overrides={}):
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.update(**config_overrides)

    if app.debug:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)
        except:
            pass

    from shitstream.queue import mod as queue_module
    app.register_blueprint(queue_module)

    db.init_app(app)
    socketio.init_app(app)

    return app
