# -*- coding: utf-8 -*-

from flask_journey import BlueprintBundle

from .planes import bp as planes
from .pilots import bp as pilots
from .routes import bp as routes

server_info = BlueprintBundle(path='/server-info')
server_info.attach_bp(routes)

v1 = BlueprintBundle(path='/api/v1')
v1.attach_bp(planes, description='Planes API, CRUD')
v1.attach_bp(pilots, description='Info about pilots')


