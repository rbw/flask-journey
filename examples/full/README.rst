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

Then point your browser to::

http://127.0.0.1:5000/api/v1/planes?wings=3

...to check out it out from a browsers point of view.

Other
-----
The Flask-Journey exposes two route listing functions in its API, one simple and one detailed. The simple version can be seen running::

$ python manage.py routes

- The other detailed one can be seen accessing the ``/routes`` endpoint
