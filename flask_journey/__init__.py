# -*- coding: utf-8 -*-

"""
    Flask-Journey
    ~~~~~~~~~~~~
    Simple Blueprint / route manager for Flask

"""

__author__ = "Robert Wikman <rbw@vault13.org>"
__version__ = "0.1.0"

from .exceptions import InvalidBasePath, IncompatibleRoute


class Route(object):
    """Creates a new route on the path specified

    :param path: route path
    """

    def __init__(self, path='/'):
        self.path = self.sanitize_path(path)
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

    def attach_bp(self, bp):
        """Attaches a blueprint

        :param bp: :class:`flask.Blueprint` object
        """

        self.blueprints.append(bp)


class Journey(object):
    """Central controller class.
    Registers blueprints and exposes `routes` property, which lists all routes added with Journey.
    :param app: App to pass directly to Journey
    """

    def __init__(self, app=None):
        self._app = None
        self._routes = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes Journey extension
        :param app: App passed from constructor or directly to init_app
        """

        self._app = app

    @property
    def routes_detailed(self):
        """Returns a detailed list of routes added with Journey

        :return: List of blueprint routes
        """

        return self._routes

    @property
    def routes_simple(self):
        """Returns a list of tuples containing endpoint-route pairs

        :return: List of route pairs
        """

        def get_full_path(p_base, p_bp, p_child):
            return "{0}{1}{2}".format(p_base, p_bp, p_child)

        routes = []

        for route in self._routes:
            base_path = route['base_path']
            for blueprint in route['blueprints']:
                bp_path = blueprint['path']
                for child in blueprint['routes']:
                    routes.append((child['endpoint'], get_full_path(base_path, bp_path, child['path'])))

        return routes

    def register_route(self, route):
        """Registers blueprints attached to the :class:`flask_journey.Route` object passed

        :param route: :class:`flask_journey.Route` object
        :raises:
            - IncompatibleRoute if the route is not of type `Route`
        """

        if not isinstance(route, Route):
            raise IncompatibleRoute('Manager object passed to register_router must be of type {0}'.format(Route))

        registered_route = {
            'base_path': route.path,
            'blueprints': []
        }

        for bp in route.blueprints:
            # Get route name (from url_prefix or name attr) and prepend with a slash
            child_path = self.get_child_name(bp)

            # Create full path to the BP route
            base_path = "{0}/{1}".format(route.path, child_path)

            # Register the BP
            blueprint = self._register_blueprint(bp, base_path, child_path)

            # Add routes for this blueprint
            blueprint['routes'] = self._get_blueprint_routes(base_path)

            # Finally, attach the blueprints to its parent
            registered_route['blueprints'].append(blueprint)

        self._routes.append(registered_route)

    def _register_blueprint(self, bp, base_path, child_path):
        """Register and return info about the registered blueprint

        :param bp: :class:`flask.Blueprint` object
        :param base_path: the URL prefix of this blueprint
        :param child_path: blueprint relative to the router path
        :return: Dict with info about the blueprint
        """

        self._app.register_blueprint(bp, url_prefix=base_path)
        return {
            'name': bp.name,
            'path': child_path,
            'import_name': bp.import_name,
            'routes': []
        }

    @staticmethod
    def get_child_name(bp):
        """Strips leading slashes from url_prefix, if it has been set, and returns. If not, return `Blueprint.name`.

        :param bp: :class:`flask.Blueprint` object
        :return: blueprint name
        """

        if bp.url_prefix and bp.url_prefix[:1] == '/':
            return bp.url_prefix.lstrip('/')

        return bp.name

    def _get_blueprint_routes(self, base_path):
        """Returns detailed information about registered blueprint routes matching the `Route` path

        :param base_path: Base path to return detailed route info for
        :return: List of route detail dicts
        """

        routes = []

        for child in self._app.url_map.iter_rules():
            if child.rule.startswith(base_path):
                relative_path = child.rule[len(base_path):]
                routes.append({
                    'path': relative_path,
                    'endpoint': child.endpoint,
                    'methods': list(child.methods)
                })

        return routes
