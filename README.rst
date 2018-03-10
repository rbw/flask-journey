Flask-Journey
=============

Lightweight extension for Flask that primarily assists with blueprint and route management, but also (de)serialization and validation in views using blueprints.

It uses and is compatible with the standard Flask blueprint system, is modular and doesn't depend on anything special.

Add an auth component and you're pretty much up and running with your REST API.


Highlights
----------

- Dead simple blueprint and route management that works with vanilla blueprints in Flask
- Drop-in replacement for ``flask.Blueprint.route`` with support for Marshmallow deserialization + validation and marshalling


Basic usage
-----------

This shows some basic usage to give you an idea of how the extension works.

Check out the **examples** directory for usable examples.


Blueprint / Route management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This component of Flask-Journey is primarily for larger applications using factories, but works in any type of Flask application.


**api/routes.py**

.. code-block:: python

  from flask_journey import Route
  from .users import bp as users_bp
  from .groups import bp as groups_bp

  v1 = Route('/api/v1')
  v1.attach_bp(users_bp, description='Users API')
  v1.attach_bp(groups_bp)


**api/app.py**

.. code-block:: python

  from flask import Flask
  from flask_journey import Journey

  from .routes import v1

  journey = Journey()
  app = Flask(__name__)
  journey.init_app(app)
  journey.register_route(v1)
  
  print(journey.routes_simple)


The route decorator
^^^^^^^^^^^^^^^^^^^

**api/users/schemas.py**

These are regular marshmallow type schemas

.. code-block:: python

  from marshmallow import Schema, fields, validate

  class QuerySchema(Schema):
      first_name = fields.String(required=False)
      last_name = fields.String(required=False)


  class UserSchema(Schema):
      id = fields.Integer(required=True)
      first_name = fields.String(required=True)
      last_name = fields.String(required=True)
      user_name = fields.String(required=True)

**api/users/views.py**

The ``flask_journey.utils.route`` decorator is used with standard Flask blueprints and enables easy (de)serialization and validation with the help of the Marshmallow library.

.. code-block:: python

  from flask import Blueprint
  from flask_journey.utils import route
  from db import create_user, get_user
  
  from .schema import UserSchema
  
  bp = Blueprint('users', __name__)

  @route(bp, '/', methods=['GET'], query_schema=QuerySchema(strict=True), marshal_with=UserSchema(many=True))
  def get_many(__query=None):
      return get_users(**__query['data'])


  @route(bp, '/', methods=['POST'], body_schema=UserSchema(strict=True), marshal_with=UserSchema())
  def create(__body=None):
      return create_user(**__body['data'])




