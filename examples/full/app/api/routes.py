# -*- coding: utf-8 -*-

from flask_journey import Route
from .planes import bp as planes
from .pilots import bp as pilots
from ._routes import bp as routes

v1 = Route('/api/v1')
v1.attach_bp(planes, description='Planes API, CRUD')
v1.attach_bp(pilots, description='Info about pilots')
v1.attach_bp(routes)
