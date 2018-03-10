# -*- coding: utf-8 -*-

from unittest import TestCase
from flask import Blueprint
from flask_journey import BlueprintBundle, InvalidBundlePath, InvalidBlueprint


class BundleTestCase(TestCase):
    def test_create_invalid_path(self):
        """Invalid paths should raise an `InvalidBundlePath` exception"""
        self.assertRaises(InvalidBundlePath, BlueprintBundle, 'test')
        self.assertRaises(InvalidBundlePath, BlueprintBundle, 'test/')
        self.assertRaises(InvalidBundlePath, BlueprintBundle, 'test/test')

    def test_create_valid_path(self):
        """Improper paths should get sanitized, valid paths should return what was provided"""

        b1_path = '/'
        b2_path = '/test///'
        b3_path = '/test/test'

        b1 = BlueprintBundle(b1_path)
        b2 = BlueprintBundle(b2_path)
        b3 = BlueprintBundle(b3_path)

        # Single slash shouldn't get stripped
        self.assertEqual(b1.path, b1_path)

        # Trailing slashes should get stripped
        self.assertEqual(b2.path, b2_path.rstrip('/'))

        # Clean paths should equal what was provided
        self.assertEqual(b3.path, b3_path)

    def test_add_bundle_description(self):
        """Bundle description should equal whatever what passed"""

        description = 'test'
        bpb = BlueprintBundle(path='/test', description=description)

        self.assertEqual(bpb.description, description)

    def test_add_blueprint_description(self):
        """Bundle description should equal whatever what passed"""

        b1_description = 'test1'
        b2_description = 'test2'

        bp1 = Blueprint('bp1', __name__)
        bp2 = Blueprint('bp2', __name__)

        bpb = BlueprintBundle(path='/test')
        bpb.attach_bp(bp1, b1_description)
        bpb.attach_bp(bp2, b2_description)

        b1_match = False
        b2_match = False

        for (bp, description) in bpb.blueprints:
            if bp == bp1 and description == b1_description:
                b1_match = True
            elif bp == bp2 and description == b2_description:
                b2_match = True

        self.assertTrue(b1_match)
        self.assertTrue(b2_match)

    def test_attach_blueprint(self):
        """Attached blueprints should end up in BlueprintBundle.blueprints"""

        bp1 = Blueprint('bp1', __name__)
        bp2 = Blueprint('bp2', __name__)

        bpb = BlueprintBundle(path='/test')
        bpb.attach_bp(bp1)
        bpb.attach_bp(bp2)

        # The bundle should contain the attached blueprints
        self.assertTrue(bpb.blueprints.__contains__, bp1)
        self.assertTrue(bpb.blueprints.__contains__, bp2)

    def test_attach_invalid_blueprint(self):
        """Attaching a non-flask.Blueprint object should raise an InvalidBlueprint exception"""

        bpb = BlueprintBundle(path='/test')
        self.assertRaises(InvalidBlueprint, bpb.attach_bp, dict())
        self.assertRaises(InvalidBlueprint, bpb.attach_bp, object())
        self.assertRaises(InvalidBlueprint, bpb.attach_bp, None)

