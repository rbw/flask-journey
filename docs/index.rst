Flask-Journey
=============

.. module:: flask_journey

The two core components of Journey, ``route`` and ``BlueprintBundle``, are not dependent on each other, however, there
might be code added in the future that will enable them to integrate.

This, and the fact that they operate in the same field was the motivation for adding both to this extension.

Installation
------------

Use pip to install the extension::

    $ pip install flask-journey


Journey Usage
-------------

*This step is only necessary if you plan on using the BlueprintBundle*

Flask-Journey is managed through a ``Journey`` instance.
If you're utilizing application factories, then you probably want to go the init_app() route:

.. code-block:: python

    from flask import Flask
    from flask_journey import Journey

    from .bundles import bundle

    app = Flask(__name__)
    journey = Journey()
    journey.attach_bundle(bundle)
    journey.init_app(app)


You may also set up ``Journey`` directly, passing a list of bundles to the constructor:

.. code-block:: python

    app = Flask(__name__)
    journey = Journey(app, bundles=[bundle1, bundle2])


Examples
========

Using the ``Journey.route`` decorator
-------------------------------------

The ``route`` component, as mentioned previously, is not dependent on the Journey blueprint manager.
However, functions decorated with ``flask_journey.route`` can of course, just as ``flask.Blueprint.route``, be added to your app with the help of Journey.


Regular marshmallow type schemas:

.. code-block:: python

    # file: api/users/schemas.py

    from marshmallow import Schema, fields, validate

    class QuerySchema(Schema):
        first_name = fields.String(required=False)
        last_name = fields.String(required=False)


    class UserSchema(Schema):
        id = fields.Integer(required=True)
        first_name = fields.String(required=True)
        last_name = fields.String(required=True)
        user_name = fields.String(required=True)



...and the ``flask_journey.route`` decorator enables simple (de)serialization and validation:

.. code-block:: python

    # api/users/views.py

    from flask import Blueprint
    from flask_journey import route
    from db import create_user, get_user

    from .schemas import UserSchema, QuerySchema

    bp = Blueprint('users', __name__)

    @route(bp, '/', methods=['GET'], query_schema=QuerySchema(strict=True), marshal_with=UserSchema(many=True))
    def get_many(__query=None):
        return get_users(**__query['data'])


    @route(bp, '/', methods=['POST'], body_schema=UserSchema(strict=True), marshal_with=UserSchema())
    def create(__body=None):
        return create_user(**__body['data'])


These can be registered either using the regular ``register_blueprint`` method of your app, or using ``BlueprintBundle`` with ``Journey.attach_bundle``.


Bundling blueprints
-------------------

There are various benefits of using the Journey BlueprintBundle, and in most cases just one BlueprintBundle is enough.

- It can be used to easily segregate your blueprint registration code from the other parts of your application.
- It helps you group blueprints in a logical manner.
- It enables you to utilize the Journey API (currently only for blueprint bundle registration and listing routes)

.. code-block:: python

    # file: api/bundles.py

    from flask_journey import BlueprintBundle

    from .users import bp as users
    from .groups import bp as groups
    from .companies import bp as companies
    from .new_feature import bp as new_feature

    v1 = BlueprintBundle(path='/api/v1', description="API v1, stable")
    v1.attach_bp(users, description='Users CRUD')
    v1.attach_bp(groups)
    v1.attach_bp(companies, description='Companies API')

    v2 = BlueprintBundle(path='/api/v2', description="API v2, beta")
    v2.attach_bp(users, description='Users CRUD')
    v2.attach_bp(groups)
    v2.attach_bp(companies, description='Companies API')
    v2.attach_bp(new_feature)


Importing bundles
-----------------

Importing and registering bundles (along with blueprints) is easy as pie:

.. code-block:: python

    # file: api/__init__.py

    from flask import Flask
    from .bundles import v1, v2

    app = Flask(__name__)
    journey = Journey()
    journey.attach_bundle(v1)
    journey.attach_bundle(v2)
    journey.init_app(app)


Real examples
-------------

Full and usable examples can be found `here <https://github.com/rbw0/flask-journey/tree/master/examples>`_


Route decorator
---------------

.. automodule:: flask_journey.utils
    :members:


Journey API
-----------

.. autoclass:: flask_journey.Journey
    :members:


BlueprintBundle API
-------------------

.. autoclass:: flask_journey.BlueprintBundle
    :members:


Exceptions
----------

.. automodule:: flask_journey.exceptions
    :members:

