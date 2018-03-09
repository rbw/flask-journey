# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_journey.utils import route
from app.core import journey

bp = Blueprint('routes', __name__)


@route(bp, '/', methods=['GET'])
def get_many():
    return jsonify(journey.routes_detailed)

