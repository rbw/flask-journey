# -*- coding: utf-8 -*-

from .exceptions import InvalidBasePath


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
        :return: sanitized path
        """

        if path[:1] != '/':
            raise InvalidBasePath('The manager base path must start with a slash')

        return path.rstrip('/')

    def attach_bp(self, bp, description=''):
        """Attaches a flask.Blueprint to the bundle

        :param bp: :class:`flask.Blueprint` object
        :param description: Optional description string
        """

        self.blueprints.append((bp, description))
