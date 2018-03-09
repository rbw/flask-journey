# -*- coding: utf-8 -*-

from flask_script import Manager
from app.api import create_app
from app.core import journey

app = create_app()

manager = Manager(app)


@manager.command
def routes():
    for route in journey.routes_simple:
        print(route)


if __name__ == "__main__":
    manager.run()
