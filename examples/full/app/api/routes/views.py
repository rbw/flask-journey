# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from app.core import journey

bp = Blueprint('routes', __name__)


@bp.route('/', methods=['GET'], strict_slashes=False)
def get_many():
    return jsonify(journey.routes_detailed)

