from flask import Flask
from flask.ext.migrate import Migrate
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()

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

    from shitstream.queue import api_bp as queue_api, mod as queue_module
    app.register_blueprint(queue_module)
    app.register_blueprint(queue_api)

    from shitstream.queue import QueueCurrentResource

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    return app
