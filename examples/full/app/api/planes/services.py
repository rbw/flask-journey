# -*- coding: utf-8 -*-

from app.fake_data.planes import data


def get_planes(min_wings=None):
    return [x for x in data if x['wings'] >= min_wings]


def get_plane(plane_id):
    return next((x for x in data if x['id'] == int(plane_id)), {})


def create_plane(plane):
    data.append(plane)
    return plane


def update_plane(plane_id, plane):
    if not get_plane(plane_id):
        return {}
    else:
        for i, item in enumerate(data):
            if item['id'] == int(plane_id):
                data[i] = plane

    return plane


def delete_plane(plane_id):
    deleted = False
    for i, item in enumerate(data):
        if item['id'] == int(plane_id):
            deleted = True
            del data[i]

    return {'success': deleted}
