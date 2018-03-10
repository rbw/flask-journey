# -*- coding: utf-8 -*-

from unittest import TestCase
from flask import Flask, Blueprint
from flask_journey import (
    BlueprintBundle, Journey, NoBundlesAttached,
    MissingBlueprints, InvalidBundlesType, IncompatibleBundle,
    DuplicateBundlePath
)


class FlaskTestCase(TestCase):
    """Mix-in class for creating the Flask application."""

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        app.logger.disabled = True
        self.app = app

        self.bundle = BlueprintBundle(path='/test')
        self.blueprint = Blueprint('test', __name__)

    def tearDown(self):
        self.app = None

    def test_constructor_direct_no_bundles(self):
        """Initializing the app directly without bundles should raise NoBundlesAttached"""
        self.assertRaises(NoBundlesAttached, Journey, self.app, [])

    def test_constructor_direct_invalid_bundles_type(self):
        """Initializing the app directly with invalid bundles type should raise InvalidBundlesType"""
        self.assertRaises(InvalidBundlesType, Journey, self.app, str())
        self.assertRaises(InvalidBundlesType, Journey, self.app, dict())
        self.assertRaises(InvalidBundlesType, Journey, self.app, None)

    def test_constructor_direct(self):
        """Initializing the app directly with a list of bundles should work"""

        bp1_name = 'test1'
        bp2_name = 'test2'

        expected_bp1_path = '/test1'
        expected_bp2_path = '/test2'

        bpb1_path = '/api/v1'
        bpb2_path = '/api/v2'

        bp1 = Blueprint(bp1_name, __name__)
        bp2 = Blueprint(bp2_name, __name__)

        bpb1 = BlueprintBundle(path=bpb1_path)
        bpb1.attach_bp(bp1)

        bpb2 = BlueprintBundle(path=bpb2_path)
        bpb2.attach_bp(bp2)

        j = Journey(self.app, bundles=[bpb1, bpb2])

        matched_bpb1 = matched_bpb2 = matched_bp1 = matched_bp2 = False

        for registered_bundle in j._registered_bundles:
            if registered_bundle['path'] == bpb1_path:
                matched_bpb1 = True
            elif registered_bundle['path'] == bpb2_path:
                matched_bpb2 = True

            for blueprint in registered_bundle['blueprints']:
                if blueprint['name'] == bp1_name and blueprint['path'] == expected_bp1_path:
                    matched_bp1 = True
                elif blueprint['name'] == bp2_name and blueprint['path'] == expected_bp2_path:
                    matched_bp2 = True

        self.assertTrue(matched_bpb1)
        self.assertTrue(matched_bpb2)
        self.assertTrue(matched_bp1)
        self.assertTrue(matched_bp2)

    def test_duplicate_bundle(self):
        """Adding a bundle for a path that already exists should raise DuplicateBundlePath"""

        bpb1_path = '/api/v1'
        bpb2_path = '/api/v1'

        bpb1 = BlueprintBundle(bpb1_path)
        bpb1.attach_bp(self.blueprint)

        bpb2 = BlueprintBundle(bpb2_path)
        bpb2.attach_bp(self.blueprint)

        j = Journey()
        j.attach_bundle(bpb1)
        self.assertRaises(DuplicateBundlePath, j.attach_bundle, bpb2)

    def test_bp_reuse(self):
        """Reusing blueprints in bundles should work"""

        bpb1_path = '/api/v1'
        bpb2_path = '/api/v2'
        bp_name = 'bp_name'
        route_ep = 'test'

        bp = Blueprint(bp_name, __name__)

        @bp.route('/test')
        def test_route():
            return False

        bpb1 = BlueprintBundle(bpb1_path)
        bpb1.attach_bp(bp)

        bpb2 = BlueprintBundle(bpb2_path)
        bpb2.attach_bp(bp)

        j = Journey()
        j.attach_bundle(bpb1)
        j.attach_bundle(bpb2)
        j.init_app(self.app)

        expected_bpb1_route = "{0}/{1}/{2}".format(bpb1_path, bp_name, route_ep)
        expected_bpb2_route = "{0}/{1}/{2}".format(bpb2_path, bp_name, route_ep)

        matched_bpb1_route = matched_bpb2_route = False

        for mapping in j.routes_simple:
            if mapping[1] == expected_bpb1_route:
                matched_bpb1_route = True
            elif mapping[1] == expected_bpb2_route:
                matched_bpb2_route = True

        self.assertTrue(matched_bpb1_route)
        self.assertTrue(matched_bpb2_route)

    def test_routes_detailed(self):
        """The Journey.routes_detailed property should return a list of bundles with blueprints and routes"""

        bp_name = 'test'
        expected_bp_path = '/test'
        bp_route_path = '/route'
        bpb_path = '/api/test'

        bp = Blueprint(bp_name, __name__)

        @bp.route(bp_route_path)
        def test_route():
            return None

        bpb = BlueprintBundle(bpb_path)
        bpb.attach_bp(bp)
        j = Journey()
        j.attach_bundle(bpb)
        j.init_app(self.app)

        regged_bpb = j.routes_detailed[0]
        regged_bp = regged_bpb['blueprints'][0]
        regged_bp_route = regged_bp['routes'][0]

        self.assertEqual(regged_bpb['path'], bpb_path)
        self.assertEqual(regged_bp['path'], expected_bp_path)
        self.assertEqual(regged_bp_route['path'], bp_route_path)

    def test_routes_simple(self):
        """The Journey.routes_simple property should return one (endpoint, route, methods) per route"""

        bp_name = 'test'
        expected_bp_path = '/test'
        bp_route_path = '/route'
        bpb_path = '/api/test'

        bp = Blueprint(bp_name, __name__)

        @bp.route(bp_route_path)
        def test_route():
            return None

        bpb = BlueprintBundle(bpb_path)
        bpb.attach_bp(bp)
        j = Journey()
        j.attach_bundle(bpb)
        j.init_app(self.app)

        expected_endpoint_name = "{0}.{1}".format(bp_name, 'test_route')
        expected_route_path = "{0}{1}{2}".format(bpb_path, expected_bp_path, bp_route_path)

        self.assertEqual(j.routes_simple[0][0], expected_endpoint_name)
        self.assertEqual(j.routes_simple[0][1], expected_route_path)

    def test_no_bundles(self):
        """Attempting to initialize Journey without bundles should raise NoBundlesAttached"""

        j = Journey()

        self.assertRaises(NoBundlesAttached, j.init_app, self.app)

    def test_incompatible_bundle(self):
        """Passing a non-BlueprintBundle object to attach_bundle should raise IncompatibleBundle"""

        j = Journey()
        self.assertRaises(IncompatibleBundle, j.attach_bundle, dict())
        self.assertRaises(IncompatibleBundle, j.attach_bundle, None)
        self.assertRaises(IncompatibleBundle, j.attach_bundle, str())

    def test_attach_bundle(self):
        """Attached bundles should be available in _attached_bundles prior to initializing"""

        b = self.bundle
        b.attach_bp(self.blueprint)

        j = Journey()
        j.attach_bundle(b)

        self.assertTrue(j._attached_bundles.__contains__, self.bundle)

    def test_init_attached_bundle(self):
        """Attached bundles should be available in _registered_bundles after initializing"""

        b = self.bundle
        b.attach_bp(self.blueprint)

        j = Journey()
        j.attach_bundle(b)
        j.init_app(self.app)

        matched_bundle = False

        for registered_bundle in j._registered_bundles:
            if registered_bundle['path'] == self.bundle.path:
                matched_bundle = True

        self.assertTrue(matched_bundle)

    def test_attach_empty_bundle(self):
        """Attempting to attach a bundle without blueprints should raise a MissingBlueprints exception"""

        j = Journey()

        self.assertRaises(MissingBlueprints, j.attach_bundle, self.bundle)

    def test_custom_blueprint_prefix(self):
        """Blueprints with a custom prefix should end up in blueprint path"""

        bp_prefix = '/test123'
        bp_name = 'test'

        bp = Blueprint(bp_name, __name__, url_prefix=bp_prefix)

        b = self.bundle
        b.attach_bp(bp)

        j = Journey()
        j.attach_bundle(self.bundle)
        j.init_app(self.app)

        matched_blueprint = False

        for registered_bundle in j._registered_bundles:
            for blueprint in registered_bundle['blueprints']:
                if blueprint['path'] == bp_prefix and blueprint['name'] == bp_name:
                    matched_blueprint = True

        self.assertTrue(matched_blueprint)

    def test_blueprint_path(self):
        """Blueprint path should equal /<name> if no url_prefix was provided"""

        bp_name = 'test'
        bp_expected_path = '/{0}'.format(bp_name)

        bp = Blueprint(bp_name, __name__)

        b = self.bundle
        b.attach_bp(bp)

        j = Journey()
        j.attach_bundle(self.bundle)
        j.init_app(self.app)

        matched_blueprint = False

        for registered_bundle in j._registered_bundles:
            for blueprint in registered_bundle['blueprints']:
                if blueprint['path'] == bp_expected_path:
                    matched_blueprint = True

        self.assertTrue(matched_blueprint)

