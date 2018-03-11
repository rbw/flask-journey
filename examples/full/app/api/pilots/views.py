# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_journey import route

from app.fake_data.pilots import get_pilots, get_pilot

from .schemas import pilot, pilots, query


bp = Blueprint('pilots', __name__)


@route(bp, '/<pilot_id>', methods=['GET'], marshal_with=pilot)
def get_one(pilot_id):
    return get_pilot(pilot_id)


@route(bp, '/', methods=['GET'], _query=query, marshal_with=pilots, validate=False)
def get_many(_query=None):
    pilot_name = _query.data.get('name', None)
    return get_pilots(pilot_name)

