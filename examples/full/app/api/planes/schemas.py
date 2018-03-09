# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, validate


class QuerySchema(Schema):
    wings = fields.Integer(required=True, validate=validate.Range(min=2, max=8))


class PlaneSchema(Schema):
    id = fields.Integer(required=True)
    wings = fields.Integer(required=True)
    name = fields.String(required=True)
