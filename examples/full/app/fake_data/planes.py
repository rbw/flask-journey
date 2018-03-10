data = [
    {
        'id': 1,
        'name': 'One cool plane',
        'wings': 5,
    },
    {
        'id': 2,
        'name': 'One very cool plane',
        'wings': 8,
    },
    {
        'id': 3,
        'name': 'Boring plane',
        'wings': 2,
    },
]


def get_planes(min_wings=None):
    return [x for x in data if x['wings'] >= min_wings]


def get_plane(plane_id):
    return next((x for x in data if x['id'] == int(plane_id)), {})


def create_plane(plane):
    data.append(plane)
    return plane


def update_plane(plane_id, plane):
    existing_plane = next((x for x in data if x['id'] == int(plane_id)), {})
    if not existing_plane:
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
