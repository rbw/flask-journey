# -*- coding: utf-8 -*-

"""
    Flask-Journey
    ~~~~~~~~~~~~
    Simple Blueprint manager for Flask

"""

__author__ = "Robert Wikman <rbw@vault13.org>"
__version__ = "0.1.2"

from .exceptions import (
    IncompatibleBundle, InvalidBundlePath, IncompatibleSchema,
    InvalidBlueprint, NoBundlesAttached, MissingBlueprints,
    InvalidBundlesType, DuplicateBundlePath
)

from .blueprint_bundle import BlueprintBundle
from .utils import route


class Journey(object):
    """Central controller class.
    Registers bundles and exposes properties for listing routes.

    :param app: App to pass directly to Journey
    :raises:
        - InvalidBundlesType if passed bundles is not of type list
    """

    def __init__(self, app=None, bundles=None):
        self._app = None
        self._registered_bundles = []
        self._attached_bundles = []

        if app is not None:
            if not isinstance(bundles, list):
                raise InvalidBundlesType('Bundles passed directly to Journey must be contained in a list')
            else:
                [self.attach_bundle(bundle) for bundle in bundles]

            self.init_app(app)

    def init_app(self, app):
        """Initializes Journey extension

        :param app: App passed from constructor or directly to init_app
        :raises:
            - NoBundlesAttached if no bundles has been attached attached

        """

        if len(self._attached_bundles) == 0:
            raise NoBundlesAttached("At least one bundle must be attached before initializing Journey")

        for bundle in self._attached_bundles:
            processed_bundle = {
                'path': bundle.path,
                'description': bundle.description,
                'blueprints': []
            }

            for (bp, description) in bundle.blueprints:
                # Register the BP
                blueprint = self._register_blueprint(app, bp, bundle.path,
                                                     self.get_child_path(bp), description)

                # Finally, attach the blueprints to its parent
                processed_bundle['blueprints'].append(blueprint)

            self._registered_bundles.append(processed_bundle)

    @property
    def routes_detailed(self):
        """Returns a detailed list bundles and its blueprints and routes

        :return: List of blueprint routes
        """

        return self._registered_bundles

    @property
    def routes_simple(self):
        """Returns simple info about registered blueprints

        :return: Tuple containing endpoint, path and allowed methods for each route
        """

        routes = []

        for bundle in self._registered_bundles:
            bundle_path = bundle['path']
            for blueprint in bundle['blueprints']:
                bp_path = blueprint['path']
                for child in blueprint['routes']:
                    routes.append(
                        (
                            child['endpoint'],
                            bundle_path + bp_path + child['path'],
                            child['methods']
                        )
                    )

        return routes

    def _bundle_exists(self, path):
        """Checks if a bundle exists at the provided path

        :param path: Bundle path
        :return: bool
        """

        for attached_bundle in self._attached_bundles:
            if path == attached_bundle.path:
                return True

        return False

    def attach_bundle(self, bundle):
        """Attaches a bundle object

        :param bundle: :class:`flask_journey.BlueprintBundle` object
        :raises:
            - IncompatibleBundle if the bundle is not of type `BlueprintBundle`
            - DuplicateBundlePath if a bundle has already been attached at the same path
            - MissingBlueprints if the bundle doesn't contain any blueprints
        """

        if not isinstance(bundle, BlueprintBundle):
            raise IncompatibleBundle('BlueprintBundle object passed to attach_bundle must be of type {0}'
                                     .format(BlueprintBundle))
        elif len(bundle.blueprints) == 0:
            raise MissingBlueprints("Bundles must contain at least one flask.Blueprint")
        elif self._bundle_exists(bundle.path):
            raise DuplicateBundlePath("Duplicate bundle path {0}".format(bundle.path))

        self._attached_bundles.append(bundle)

    def _register_blueprint(self, app, bp, bundle_path, child_path, description):
        """Register and return info about the registered blueprint

        :param bp: :class:`flask.Blueprint` object
        :param bundle_path: the URL prefix of the bundle
        :param child_path: blueprint relative to the bundle path
        :return: Dict with info about the blueprint
        """

        base_path = bundle_path + child_path

        app.register_blueprint(bp, url_prefix=base_path)

        return {
            'name': bp.name,
            'path': child_path,
            'import_name': bp.import_name,
            'description': description,
            'routes': self.get_blueprint_routes(app, base_path)
        }

    @staticmethod
    def get_child_path(bp):
        """Strips leading slashes from url_prefix, if it has been set, and returns. If not, return `Blueprint.name`.

        :param bp: :class:`flask.Blueprint` object
        :return: blueprint name
        """

        return bp.url_prefix or '/' + bp.name

    @staticmethod
    def get_blueprint_routes(app, base_path):
        """Returns detailed information about registered blueprint routes matching the `BlueprintBundle` path

        :param app: App instance to obtain rules from
        :param base_path: Base path to return detailed route info for
        :return: List of route detail dicts
        """

        routes = []

        for child in app.url_map.iter_rules():
            if child.rule.startswith(base_path):
                relative_path = child.rule[len(base_path):]
                routes.append({
                    'path': relative_path,
                    'endpoint': child.endpoint,
                    'methods': list(child.methods)
                })

        return routes
