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

The extension is managed through a ``Journey`` instance.
If utilizing application factories, then you probably want to go the init_app() route:

.. code-block:: python

    from flask import Flask
    from flask_journey import Journey

    from .bundles import bundle1, bundle2

    app = Flask(__name__)
    journey = Journey()
    journey.attach_bundle(bundle1)
    journey.attach_bundle(bundle2)
    journey.init_app(app)


You may also set up ``Journey`` directly, passing a list of bundles its constructor:

.. code-block:: python

    app = Flask(__name__)
    journey = Journey(app, bundles=[bundle1, bundle2])




The route decorator
===================

The ``route`` component, as mentioned previously, is not dependent on the Journey blueprint manager.
However, functions decorated with ``flask_journey.route`` can of course, just as ``flask.Blueprint.route``, be added to your app with the help of Journey.


**Marshmallow compatible schemas:**

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


    users = UserSchema(many=True)
    user = UserSchema()
    query = QuerySchema()


**...with the flask_journey.route decorator enables simple (de)serialization and validation:**

.. code-block:: python

    # api/users/controllers.py

    from flask import Blueprint
    from flask_journey import route

    from .services import create_user, get_user, update_user
    from .schemas import user, users, query

    bp = Blueprint('users', __name__)

    @route(bp, '/', methods=['GET'], _query=query, marshal_with=users)
    def get_many(_query):
        return get_users(_query.data)


    @route(bp, '/', methods=['POST'], _body=user, marshal_with=user)
    def create(_body):
        return create_user(_body.data)


    @route(bp, '/<user_id>', methods=['PUT'], _body=user, marshal_with=user)
    def update(user_id, _body):
        return update_user(user_id, _body.data)

Blueprints
==========


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
    from .stuff import bp as stuff

    v1 = BlueprintBundle(path='/api/v1', description="API v1, stable")
    v1.attach_bp(users, description='Users CRUD')
    v1.attach_bp(groups)
    v1.attach_bp(companies, description='Companies API')

    other = BlueprintBundle(path='/other')
    other.attach_bp(stuff)


Importing bundles
-----------------

Importing and registering bundles (along with blueprints) is easy as pie:

.. code-block:: python

    # file: api/__init__.py

    from flask import Flask
    from .bundles import v1, other

    app = Flask(__name__)
    journey = Journey()
    journey.attach_bundle(v1)
    journey.attach_bundle(other)
    journey.init_app(app)



API Documentation
=================


Journey API
-----------

.. autoclass:: flask_journey.Journey
    :members:


Route decorator
---------------

.. automodule:: flask_journey.utils
    :members:


BlueprintBundle API
-------------------

.. autoclass:: flask_journey.BlueprintBundle
    :members:


Exceptions
----------

.. automodule:: flask_journey.exceptions
    :members:

