Full example
------------

This example shows how a structured Flask application can utilize the Flask-Journey extension for:

- Simple route / blueprint management
- Deserialization
- Validation
- Marshalling


Note that the `routes` endpoint uses the regular ``route`` decorator from ``flask.Blueprint``. This is intentional to show that Flask-Journey doesn't depend on its own ``route`` implementation.


Preparations
------------

Install dependencies::

$ pip install -r requirements.txt


Running
-------

Start the server using the manager::

$ python manage.py runserver


Other
-----
The Flask-Journey exposes two route listing functions in its API, one simple and one detailed. The simple version can be seen running::

$ python manage.py routes

- The other detailed one can be seen accessing the ``/routes`` endpoint
