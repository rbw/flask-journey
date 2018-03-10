.. code-block::

         _                                  
        (_)___  __  ___________  ___  __  __
       / / __ \/ / / / ___/ __ \/ _ \/ / / /
      / / /_/ / /_/ / /  / / / /  __/ /_/ / 
   __/ /\____/\__,_/_/  /_/ /_/\___/\__, /  
  /___/ Flask blueprint management /____/

.. image:: https://coveralls.io/repos/github/rbw0/flask-journey/badge.svg?branch=master
    :target: https://coveralls.io/github/rbw0/flask-journey?branch=master
.. image:: https://travis-ci.org/rbw0/flask-journey.svg?branch=master
    :target: https://travis-ci.org/rbw0/flask-journey
.. image:: https://badge.fury.io/py/flask-journey.svg
    :target: https://pypi.python.org/pypi/flask-journey
.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :target: https://opensource.org/licenses/MIT


Description
-----------

Provides a clean, declarative way of importing and managing blueprints and creating routes.
In addition to this, it also enables simple and consistent methods of (de)serialization and validation in blueprint enabled views.

It uses the standard Flask blueprint system, is modular and doesn't depend on anything special.


This along with an auth component is pretty much all you need for a solid REST API foundation. 


Highlights
----------

- Dead simple blueprint and route management that works with vanilla blueprints in Flask
- Drop-in replacement for ``flask.Blueprint.route`` with support for Marshmallow


Installing
----------

$ pip install flask-journey


Basic usage
-----------

This shows some super basic usage to give you an idea of how the extension works.

Check out the **examples** directory for actually usable examples.


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

The ``flask_journey.route`` decorator is used with standard Flask blueprints and enables easy (de)serialization and validation with the help of the Marshmallow library.

.. code-block:: python

  from flask import Blueprint
  from flask_journey import route
  from db import create_user, get_user
  
  from .schema import UserSchema
  
  bp = Blueprint('users', __name__)

  @route(bp, '/', methods=['GET'], query_schema=QuerySchema(strict=True), marshal_with=UserSchema(many=True))
  def get_many(__query=None):
      return get_users(**__query['data'])


  @route(bp, '/', methods=['POST'], body_schema=UserSchema(strict=True), marshal_with=UserSchema())
  def create(__body=None):
      return create_user(**__body['data'])



Blueprint / Route management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This component of Flask-Journey is primarily for larger applications using factories, but works in any type of Flask application.


**api/bundles.py**

.. code-block:: python

  from flask_journey import BlueprintBundle
  from .users import bp as users_bp
  from .groups import bp as groups_bp

  v1 = BlueprintBundle(path='/api/v1')
  v1.attach_bp(users_bp, description='Users API')
  v1.attach_bp(groups_bp)


**api/__init__.py**

.. code-block:: python

  from flask import Flask
  from flask_journey import Journey

  from .bundles import v1

  app = Flask(__name__)

  journey = Journey()
  journey.attach_bundle(v1)

  journey.init_app(app)
  
  print(journey.routes_simple)



Compatibility
-------------
- Python 2 and 3
- Flask > 0.9

Author
------
Created by Robert Wikman <rbw@vault13.org> in 2018

JetBrains
---------
Thank you `Jetbrains <http://www.jetbrains.com>`_ for creating pycharm and for providing me with free licenses

