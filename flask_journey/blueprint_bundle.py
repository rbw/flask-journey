# -*- coding: utf-8 -*-

from flask import Blueprint

from .utils import sanitize_path
from .exceptions import InvalidBlueprint


class BlueprintBundle(object):
    """Creates a BlueprintBundle at the path specified

    :param path: blueprint base path
    """

    def __init__(self, path='/', description=''):
        self.path = sanitize_path(path)
        self.description = description
        self.blueprints = []

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
