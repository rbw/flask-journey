Planes API
----------

This API heavily utilizes Marshmallow and exposes full CRUD functionality with:

- Query string / parameters deserialization + validation (route._query)
- JSON data (body) deserialization + validation (route._body)
- Response marshalling (route.marshal_with)
