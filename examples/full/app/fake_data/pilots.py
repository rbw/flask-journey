data = [
    {
        'id': 1,
        'name': 'Rick',
    },
    {
        'id': 2,
        'name': 'Morty',
    },
    {
        'id': 3,
        'name': 'Jerry',
    },
]


def get_pilots(name=None):
    if name:
        return [x for x in data if x['name'] == name]

    return data


def get_pilot(pilot_id):
    return next((x for x in data if x['id'] == int(pilot_id)), {})
