# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, validate


class QuerySchema(Schema):
    min_wings = fields.Integer(required=True, validate=validate.Range(min=2, max=8))


class PlaneSchema(Schema):
    id = fields.Integer(required=True)
    wings = fields.Integer(required=True)
    name = fields.String(required=True)


planes = PlaneSchema(many=True)
plane = PlaneSchema()
query = QuerySchema()
