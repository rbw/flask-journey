# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_journey.utils import route

from app.fake_data.pilots import get_pilots, get_pilot

from .schemas import PilotSchema, QuerySchema


bp = Blueprint('pilots', __name__)


@route(bp, '/<plane_id>', methods=['GET'], marshal_with=PilotSchema())
def get_one(pilot_id):
    return get_pilot(pilot_id)


@route(bp, '/', methods=['GET'], query_schema=QuerySchema(strict=False), marshal_with=PilotSchema(many=True))
def get_many(__query=None):
    pilot_name = __query['data'].get('name', None)
    return get_pilots(pilot_name)

