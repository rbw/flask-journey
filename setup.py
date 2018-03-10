# -*- coding: utf-8 -*-

"""
flask-journey
------------

Lightweight extension for Flask that primarily assists with blueprint and route management,
but also (de)serialization and validation in API routes.

"""

import io
import ast

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    """ Parses main module and fetches version attribute from the syntax tree

    :return: flask-journey version

    """
    with io.open('flask_journey/__init__.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with io.open('README.rst') as readme:
    setup(
        name='flask-journey',
        version=get_version(),
        url='https://github.com/rbw0/flask-journey',
        license='MIT',
        author='Robert Wikman',
        author_email='rbw@vault13.org',
        maintainer='Robert Wikman',
        maintainer_email='rbw@vault13.org',
        description='Flask blueprint management',
        download_url='https://github.com/rbw0/flask-journey/tarball/%s' % get_version(),
        long_description=readme.read(),
        packages=['flask_journey'],
        zip_safe=False,
        include_package_data=True,
        platforms='any',
        install_requires=[
            'Flask',
            'marshmallow',
            'furl',
            'Flask-Sphinx-Themes',
        ],
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
