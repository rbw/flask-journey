# -*- coding: utf-8 -*-

from flask import Blueprint
from .exceptions import InvalidBundlePath, InvalidBlueprint


class BlueprintBundle(object):
    """Creates a BlueprintBundle at the path specified

    :param path: blueprint base path
    """

    def __init__(self, path='/', description=''):
        self.path = self.sanitize_path(path)
        self.description = description
        self.blueprints = []

    @staticmethod
    def sanitize_path(path):
        """Performs sanitation of the route path after validating

        :param path: path to sanitize
        :return: path
        :raises:
            - InvalidBundlePath if the path doesn't start with a slash
        """

        if path[:1] != '/':
            raise InvalidBundlePath('The bundle path must start with a slash')
        elif len(path) == 1:
            return path

        return path.rstrip('/')

    def attach_bp(self, bp, description=''):
        """Attaches a flask.Blueprint to the bundle

        :param bp: :class:`flask.Blueprint` object
        :param description: Optional description string
        :raises:
            - InvalidBlueprint if the Blueprint is not of type `flask.Blueprint`
        """

        if not isinstance(bp, Blueprint):
            raise InvalidBlueprint('Blueprints attached to the bundle must be of type {0}'.format(Blueprint))

        self.blueprints.append((bp, description))
