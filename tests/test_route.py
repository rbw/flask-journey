# -*- coding: utf-8 -*-

import json

from unittest import TestCase
from flask import Flask, Blueprint
from flask_journey import route, IncompatibleSchema
from marshmallow import Schema, fields, validate


class QuerySchema(Schema):
    p1 = fields.Integer(required=True, validate=validate.Range(min=2, max=8))
    p2 = fields.Integer(required=False)


class BodySchema(Schema):
    p1 = fields.Integer(required=True)
    p2 = fields.String(required=True)


class OutputSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


class FlaskTestCase(TestCase):
    """Mix-in class for creating the Flask application."""
    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        app.logger.disabled = True
        self.app = app
        self.client = self.app.test_client()
        self.blueprint = Blueprint('test', __name__)

    def test_query_schema(self):
        app = self.app
        bp = Blueprint('test', __name__)

        test_p1_value = 3
        test_p2_value = 3

        expected_output = {
            'id': 1,
            'name': 'test'
        }

        @route(bp, '/test', query_schema=QuerySchema(strict=True), marshal_with=OutputSchema())
        def get_with_query(**kwargs):
            q = kwargs['__query']['data']
            self.assertEqual(q['p1'], test_p1_value)
            self.assertEqual(q['p2'], test_p2_value)
            return expected_output

        app.register_blueprint(bp)

        response = self.client.get('/test?p1={0}&p2={1}'.format(test_p1_value, test_p2_value))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data, expected_output)

    def test_query_missing_required(self):
        app = self.app
        bp = Blueprint('test', __name__)

        missing_key = 'p1'

        @route(bp, '/test', query_schema=QuerySchema(strict=True))
        def get_with_query(**kwargs):
            return json.dumps({})

        app.register_blueprint(bp)

        response = self.client.get('/test')
        data = json.loads(response.get_data(as_text=True))

        response_has_key = missing_key in data

        self.assertTrue(response_has_key)

    def test_body_schema(self):
        app = self.app
        bp = Blueprint('test', __name__)

        test_payload = {'p1': 1, 'p2': 'test2'}

        expected_output = {
            'id': 1,
            'name': 'test'
        }

        @route(bp, '/test', methods=['POST'], body_schema=BodySchema(strict=True), marshal_with=OutputSchema())
        def get_with_query(**kwargs):
            body = kwargs['__body']['data']
            self.assertEqual(body, test_payload)
            return expected_output

        app.register_blueprint(bp)

        response = self.client.post('/test',
                                    data=json.dumps(test_payload),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data, expected_output)

    def test_body_missing_required(self):
        app = self.app
        bp = Blueprint('test', __name__)

        missing_key = 'p1'
        test_payload = {'p2': 'test2'}

        expected_output = {
            'id': 1,
            'name': 'test'
        }

        @route(bp, '/test', methods=['POST'], body_schema=BodySchema(strict=True), marshal_with=OutputSchema())
        def get_with_query(**kwargs):
            return expected_output

        app.register_blueprint(bp)

        response = self.client.post('/test',
                                    data=json.dumps(test_payload),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        response_has_key = missing_key in data

        self.assertTrue(response_has_key)

    def test_without_schemas(self):
        app = self.app
        bp = Blueprint('test', __name__)

        expected_output = {
            'id': 1,
            'name': 'test'
        }

        @route(bp, '/test')
        def get_with_query():
            return json.dumps(expected_output)

        app.register_blueprint(bp)

        response = self.client.get('/test')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data, expected_output)

    def test_invalid_body_schema(self):
        bp = Blueprint('test', __name__)
        kwargs = {'body_schema': dict()}

        self.assertRaises(IncompatibleSchema, route, bp, '/test', **kwargs)

    def test_invalid_query_schema(self):
        bp = Blueprint('test', __name__)
        kwargs = {'query_schema': dict()}

        self.assertRaises(IncompatibleSchema, route, bp, '/test', **kwargs)

    def test_invalid_marshal_with_schema(self):
        bp = Blueprint('test', __name__)
        kwargs = {'marshal_with': dict()}

        self.assertRaises(IncompatibleSchema, route, bp, '/test', **kwargs)
