# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class QuerySchema(Schema):
    name = fields.String(required=False)


class PilotSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


pilots = PilotSchema(many=True)
pilot = PilotSchema()
query = QuerySchema()
