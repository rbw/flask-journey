Flask-Journey
=============

Lightweight extension for Flask that primarily assists with blueprint and route management, but also (de)serialization and validation in API routes.

It uses and is compatible with the standard Flask blueprint system, is modular and doesn't depend on anything special.

Highlights
----------

- Dead simple blueprint and route management that works with vanilla blueprints in Flask
- Drop-in replacement for ``flask.Blueprint.route`` with support for Marshmallow deserialization + validation and marshalling

Blueprint / Route management
----------------------------

The blueprint management component of Flask-Journey is primarily for larger applications with application factories, but works in any type of Flask application.


file ``routes.py``::

from .users_api import 

