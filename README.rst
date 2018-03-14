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

- Clean and simple way of importing and managing blueprints
- Drop-in replacement for ``flask.Blueprint.route`` with support for ``marshmallow`` and ``marshmallow_sqlalchemy`` for all your (de)serialization and needs.

Installing
----------

$ pip install flask-journey


Documentation
-------------
The documentation can be found `here <http://flask-journey.readthedocs.org/>`_


Quick taste 
-----------

Shows some examples of ``@route`` and ``BlueprintBundle`` + ``Journey``

@route
^^^^^^

.. code-block:: python
    
    # file: api/users/views.py
    
    from flask import Blueprint
    from flask_journey import route
    from .db import create_user, get_user
    from .schemas import user, users, query

    bp = Blueprint('users', __name__)

    @route(bp, '/', methods=['GET'], _query=query, marshal_with=users)
    def get_many(_query):
        return get_users(_query.data)


    @route(bp, '/', methods=['POST'], _body=user, marshal_with=user)
        def create(_body):
            return create_user(_body.data)            


BlueprintBundle
^^^^^^^^^^^^^^^

.. code-block:: python

    # file: api/bundles.py

    from flask_journey import BlueprintBundle
    from .users.views import bp as users_bp

    v1 = BlueprintBundle(path='/api/v1')
    v1.attach_bp(users_bp, description='Users API')


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

*Will add more shortly (simpler ones and marshmallow-sqlalchemy)*


Compatibility
-------------
- Python 2 and 3
- Flask > 0.7

Author
------
Created by Robert Wikman <rbw@vault13.org> in 2018

JetBrains
---------
Thank you `Jetbrains <http://www.jetbrains.com>`_ for creating pycharm and for providing me with free licenses

