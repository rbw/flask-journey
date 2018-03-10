The API app
-----------

#. Blueprints from the API packages are imported in ``routes.py`` and attached to a ``Route``
#. The ``Route`` instance is then imported in the app and registered using ``Journey.register_route``


Check out the ``planes`` package for a full CRUD experience!
