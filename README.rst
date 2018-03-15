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

Extension for Flask focusing on three important areas for REST APIs:

* validation
* (de)serialization
* blueprint/route management


Flask-journey makes the process of validating and (de)serializing data to/from python objects simple and elegant with the **Journey.route** decorator - a drop-in replacement for Flask's Blueprint.route, assisted by the fantastic **Marshmallow** library.

The extension's other component, **BlueprintBundle**, helps segregate, group and register blueprints with ease while also providing methods for listing routes, either in basic form or detailed JSON.


Installing
----------

.. code-block::

    pip install flask-journey


Documentation
-------------
The documentation can be found `here <http://flask-journey.readthedocs.org/>`_


Quick taste
-----------

Some examples of ``@route`` and ``BlueprintBundle`` + ``Journey``

@route
^^^^^^

.. code-block:: python

    # file: api/users/views.py

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


BlueprintBundle
^^^^^^^^^^^^^^^

.. code-block:: python

    # file: api/bundles.py

    from flask_journey import BlueprintBundle
    from .users.views import bp as users
    from .groups.views import bp as groups

    v1 = BlueprintBundle(path='/api/v1')
    v1.attach_bp(users, description='Users API')
    v1.attach_bp(groups, description='Groups API')


Journey
^^^^^^^

.. code-block:: python

    # file: api/__init__.py

    from flask import Flask
    from flask_journey import Journey

    from .bundles import v1

    def create_app():
        app = Flask(__name__)
        journey = Journey()
        journey.attach_bundle(v1)
        journey.init_app(app)

        print(journey.routes_simple)

        return app


Full examples
-------------
Working examples can be found `here <https://github.com/rbw0/flask-journey/tree/master/examples>`_

*Will add more shortly*


Compatibility
-------------
- Python >= 2.7 or >= 3.4
- Flask > 0.7

Author
------
Created by Robert Wikman <rbw@vault13.org> in 2018

JetBrains
---------
Thank you `Jetbrains <http://www.jetbrains.com>`_ for creating pycharm and providing me with free licenses

