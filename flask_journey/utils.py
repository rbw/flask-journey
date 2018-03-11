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


def route(bp, *args, **kwargs):
    """Journey route decorator

    Enables simple serialization, deserialization and validation of Flask routes with the help of Marshmallow.

    :param bp: :class:`flask.Blueprint` object
    :param args: args to pass along to `Blueprint.route`
    :param kwargs:
        - :strict_slashes: Enable / disable strict slashes (default False)
        - :_query: Deserialize Query string with this schema
        - :_body: Deserialize JSON body with this schema
        - :marshal_with: Serialize the output with this schema
        - :validate: Set to False to disable schema validation
    :raises:
        - ValidationError if the query parameters or JSON body fails validation
    """

    kwargs['strict_slashes'] = kwargs.pop('strict_slashes', False)
    body = _validate_schema(kwargs.pop('_body', None))
    query = _validate_schema(kwargs.pop('_query', None))
    output = _validate_schema(kwargs.pop('marshal_with', None))
    validate = kwargs.pop('validate', True)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*inner_args, **inner_kwargs):
            """If a schema (_body and/or _query) was supplied to the route decorator, the deserialized
            :class`marshmallow.Schema` object is injected into the decorated function's kwargs."""

            try:
                if query is not None:
                    query.strict = validate
                    url = furl(request.url)
                    inner_kwargs['_query'] = query.load(data=url.args)

                if body is not None:
                    body.strict = validate
                    json_data = request.get_json()
                    inner_kwargs['_body'] = body.load(data=json_data)

            except ValidationError as err:
                return jsonify(err.messages), 422

            if output:
                data = output.dump(f(*inner_args, **inner_kwargs))
                return jsonify(data[0])

            return f(*inner_args, **inner_kwargs)

        return f

    return decorator
