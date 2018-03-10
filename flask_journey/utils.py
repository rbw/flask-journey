# -*- coding: utf-8 -*-

from functools import wraps
from flask import jsonify, request
from marshmallow import ValidationError, Schema
from .exceptions import IncompatibleSchema
from furl import furl


def _validate_schema(obj):
    """Ensures the passed schema instance is compatible

    :param obj: object to validate
    :return: obj
    :raises:
        - IncompatibleSchema if the passed schema is of an incompatible type
    """

    if obj is not None and not isinstance(obj, Schema):
        raise IncompatibleSchema('Schema must be of type {0}'.format(Schema))

    return obj


def route(bp, *args, strict_slashes=False,
          body_schema=None, query_schema=None, marshal_with=None, **kwargs):

    """Journey route decorator

    Enables simple serialization, deserialization and validation of Flask routes with the help of Marshmallow.

    If a schema (body_schema and/or query_schema) was passed to the decorator, the corresponding
    :class`marshmallow.Schema` object gets passed to the decorated function:

    __query - kwarg if `query_schema` was passed
    __body - kwarg if `body_schema` was passed


    :param bp: :class:`flask.Blueprint` object
    :param strict_slashes: Enable / disable strict slashes (default False)
    :param body_schema: Deserialize JSON body with this schema
    :param query_schema: Deserialize Query string with this schema
    :param marshal_with: Serialize the output with this schema
    :param args: args to pass along to `Blueprint.route`
    :param kwargs: kwargs to pass along to `Blueprint.route`
    """

    kwargs['strict_slashes'] = strict_slashes
    body_schema = _validate_schema(body_schema)
    query_schema = _validate_schema(query_schema)
    marshal_with = _validate_schema(marshal_with)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*inner_args, **inner_kwargs):
            try:
                if query_schema:
                    url = furl(request.url)
                    qs_data, qs_errors = query_schema.load(data=url.args)
                    inner_kwargs['__query'] = {'data': qs_data, 'errors': qs_errors}

                if body_schema:
                    json_data = request.get_json()
                    bs_data, bs_errors = body_schema.load(data=json_data)
                    inner_kwargs['__body'] = {'data': bs_data, 'errors': bs_errors}

            except ValidationError as err:
                return jsonify(err.messages), 422

            if marshal_with:
                data = marshal_with.dump(f(*inner_args, **inner_kwargs))
                return jsonify(data[0])

            return f(*inner_args, **inner_kwargs)

        return f

    return decorator
