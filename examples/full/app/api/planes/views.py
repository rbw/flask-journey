# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_journey import route

from app.fake_data.planes import get_plane, get_planes, create_plane, update_plane, delete_plane

from .schemas import plane, planes, query


bp = Blueprint('silly_planes', __name__, url_prefix='/planes')


@route(bp, '/<plane_id>', methods=['GET'], marshal_with=plane)
def get_one(plane_id):
    return get_plane(plane_id)


@route(bp, '/<plane_id>', methods=['PUT'], _body=plane, marshal_with=plane)
def update(plane_id, _body):
    return update_plane(plane_id, _body.data)


@route(bp, '/<plane_id>', methods=['DELETE'])
def delete(plane_id):
    return jsonify(delete_plane(plane_id))


@route(bp, '/', methods=['GET'], _query=query, marshal_with=planes)
def get_many(_query):
    return get_planes(_query.data['min_wings'])


@route(bp, '/', methods=['POST'], _body=plane, marshal_with=plane)
def create(_body):
    return create_plane(_body.data)


