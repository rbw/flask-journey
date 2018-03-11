# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import flask_journey

extensions = ['sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'
project = u'flask-journey'
copyright = u'2018, Robert Wikman'

version = release = flask_journey.__version__

exclude_patterns = ['_build']

pygments_style = 'sphinx'
html_theme_options = {'github_fork': 'rbw0/flask-journey', 'index_logo': False}

html_theme = 'flask'

htmlhelp_basename = 'flask-journeydoc'

latex_documents = [
  ('index', 'flask-journey.tex', u'Flask-Journey Documentation',
   u'Robert Wikman', 'manual'),
]

man_pages = [
    ('index', 'flask-journey', u'Flask-Journey Documentation',
     [u'Robert Wikman'], 1)
]
