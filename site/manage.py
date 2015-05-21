#!/usr/bin/env python

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, Shell
from flask.ext.script.commands import Clean, ShowUrls
from shitstream import create_app, socketio
from veejay import veejay

app = create_app()
manager = Manager(app)


@manager.command
def runserver():
    socketio.run(app, host=app.config.get('HOST'), port=app.config.get('PORT'))


@manager.command
def runveejay():
    veejay.run()

manager.add_command("shell", Shell())
manager.add_command("clean", Clean())
manager.add_command("showurls", ShowUrls())

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
