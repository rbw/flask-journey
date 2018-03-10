Planes API
----------

This API heavily utilizes marshmallow and exposes full CRUD functionality with:

- Query string / parameters validation and deserialization (route.query_schema)
- JSON data (body) validation and deserialization (route.body_schema)
- Response marshalling (route.marshal_with)
