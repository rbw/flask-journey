# -*- coding: utf-8 -*-

from app import factory
from app.core import journey

from .routes import v1


def create_app():
    app = factory.create_app(__name__)

    journey.init_app(app)
    journey.register_route(v1)

    return app
