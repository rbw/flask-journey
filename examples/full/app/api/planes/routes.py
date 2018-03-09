# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_journey.utils import route

from app.fake_data.planes import get_plane, get_planes, create_plane, upsert_plane, delete_plane

from .schemas import PlaneSchema, QuerySchema


bp = Blueprint('silly_planes', __name__, url_prefix='/planes')


@route(bp, '/<plane_id>', methods=['GET'], marshal_with=PlaneSchema())
def get_one(plane_id):
    return get_plane(plane_id)


@route(bp, '/<plane_id>', methods=['PUT'], body_schema=PlaneSchema(strict=True), marshal_with=PlaneSchema())
def upsert(plane_id, __body=None):
    return upsert_plane(plane_id, __body['data'])


@route(bp, '/<plane_id>', methods=['DELETE'])
def delete(plane_id):
    return jsonify(delete_plane(plane_id))


@route(bp, '/', methods=['GET'], query_schema=QuerySchema(strict=True), marshal_with=PlaneSchema(many=True))
def get_many(__query=None):
    return get_planes(__query['data']['wings'])


@route(bp, '/', methods=['POST'], body_schema=PlaneSchema(strict=True), marshal_with=PlaneSchema())
def create(__body=None):
    return create_plane(__body['data'])


