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
In addition to this, the extension also enables simple and consistent methods of (de)serialization and validation in blueprint enabled views.

It uses the standard Flask blueprint system, is modular and doesn't depend on anything special.


This along with an auth component is pretty much all you need for a solid REST API foundation. 


Highlights
----------

- Dead simple blueprint and route management that works with vanilla blueprints in Flask
- Drop-in replacement for ``flask.Blueprint.route`` with support for Marshmallow


Installing
----------

$ pip install flask-journey


Documentation
-------------
The documentation can be found `here <http://flask-journey.readthedocs.org/>`_

Full examples
-------------
Working examples can be found `here <https://github.com/rbw0/flask-journey/tree/master/examples>`_

*Will add more shortly (simpler ones and marshmallow-sqlalchemy)*

Quick taste 
-----------

This shows a simple example Journey's BlueprintBundle component.

.. code-block:: python

  from flask_journey import BlueprintBundle
  from .users import bp as users_bp
  from .groups import bp as groups_bp

  v1 = BlueprintBundle(path='/api/v1')
  v1.attach_bp(users_bp, description='Users API')
  v1.attach_bp(groups_bp)



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

