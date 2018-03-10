The API app
-----------

#. Blueprints from the API packages are imported in ``bundles.py`` and attached to a ``BlueprintBundle``
#. The ``BlueprintBundle`` instance is then imported in the app and registered using ``Journey.attach_bundle``


Check out the ``planes`` package for a full CRUD experience!
