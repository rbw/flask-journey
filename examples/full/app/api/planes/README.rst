Planes API
----------

This API heavily utilizes Marshmallow and exposes full CRUD functionality with:

- Query string / parameters deserialization + validation (route.query_schema)
- JSON data (body) validation and deserialization (route.body_schema)
- Response marshalling (route.marshal_with)
