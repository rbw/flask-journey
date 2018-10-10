Full example
------------

This example shows how a structured Flask application can utilize the Flask-Journey extension for:

- blueprint management
- (de)serialization
- validation


Note that the **routes controller** uses the regular ``route`` decorator from ``flask.Blueprint``. This is intentional to show that Flask-Journey works seamlessly with vanilla Flask blueprints.


Preparations
------------

Install dependencies::

$ pip install -r requirements.txt


Running
-------

Start the server using the manager::

$ python manage.py runserver


============================== ============== ================
Name                           Default value  Description
============================== ============== ================
list routes with details       GET            http://127.0.0.1:5000/server-info/routes
planes with 3 or more wings    GET            http://127.0.0.1:5000/api/v1/planes?min_wings=3
get pilot by id                GET            http://127.0.0.1:5000/api/v1/pilots/1
update plane #3                PUT            http://127.0.0.1:5000/api/v1/planes/3
delete plane #2                DELETE         http://127.0.0.1:5000/api/v1/planes/2
create a new plane             POST           http://127.0.0.1:5000/api/v1/planes
get pilot by name              GET            http://127.0.0.1:5000/api/v1/pilots?name=Morty
============================== ============== ================


Other
-----
The Flask-Journey exposes two route listing functions in its API, one simple and one detailed. The simple version can be seen by running::

$ python manage.py routes

