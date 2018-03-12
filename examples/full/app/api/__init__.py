# -*- coding: utf-8 -*-

from app import factory
from app.core import journey

from .bundles import v1, server_info


def create_app():
    app = factory.create_app(__name__)

    journey.attach_bundle(v1)
    journey.attach_bundle(server_info)
    journey.init_app(app)

    return app
