#!/usr/bin/env python

from flask.ext.script import Manager, Server, Shell
from flask.ext.script.commands import Clean, ShowUrls
from shitstream import create_app, socketio

app = create_app()
manager = Manager(app)

@manager.command
def runserver():
    socketio.run(app)

manager.add_command("shell", Shell())
manager.add_command("clean", Clean())
manager.add_command("showurls", ShowUrls())

if __name__ == "__main__":
    manager.run()
