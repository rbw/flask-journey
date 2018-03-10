# -*- coding: utf-8 -*-

from app import factory
from app.core import journey

from .bundles import v1


def create_app():
    app = factory.create_app(__name__)

    journey.attach_bundle(v1)
    journey.init_app(app)

    return app
