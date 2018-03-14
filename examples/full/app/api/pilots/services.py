# -*- coding: utf-8 -*-

from app.fake_data.pilots import data


def get_pilots(name=None):
    if name:
        return [x for x in data if x['name'] == name]

    return data


def get_pilot(pilot_id):
    return next((x for x in data if x['id'] == int(pilot_id)), {})
