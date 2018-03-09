# -*- coding: utf-8 -*-

from flask import Flask


def create_app(package_name):
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('app.settings')

    return app

