# -*- coding: utf-8 -*-


class InvalidBundlePath(Exception):
    pass


class InvalidBundlesType(Exception):
    pass


class IncompatibleSchema(Exception):
    pass


class IncompatibleBundle(Exception):
    pass


class InvalidBlueprint(Exception):
    pass


class NoBundlesAttached(Exception):
    pass


class MissingBlueprints(Exception):
    pass


class DuplicateBundlePath(Exception):
    pass
