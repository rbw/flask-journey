Full example
------------

This example shows how a structure suitable for large-scale applications can utilize the Flask-Journey extension for:
- Simple route / blueprint management
- Deserialization
- Validation
- Marshalling


Note that the `routes` endpoint uses the regular `route` decorator from `flask.Blueprint`. This is intentional to show that Flask-Journey doesn't depend on its own `route` implementation.


Preparations
------------

  $ pip install -r requirements.txt


Running
-------

  $ python manage.py runserver


Other
-----

    $ python manage.py routes
