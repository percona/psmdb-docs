#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath("../"))
from conf import *
extensions.append('sphinx_gitstamp')
extensions.append('sphinx_copybutton')
extensions.append('sphinx_tabs.tabs')
html_sidebars['**']=['globaltoc.html', 'searchbox.html', 'localtoc.html', 'logo-text.html']
html_theme = 'sphinx_material'
html_theme_options = {
    'base_url': 'http://bashtage.github.io/sphinx-material/',
    'repo_url': 'https://github.com/percona/psmdb-docs',
    'repo_name': 'percona/psmdb-docs',
    'color_accent': 'grey',
    'color_primary': 'orange',
    'google_analytics_account': 'UA-343802-3',
    'globaltoc_collapse': True,
    'version_dropdown': True,
    'version_dropdown_text': 'Versions',
    'version_info': {
        "3.6": "https://docs.percona.com/percona-server-for-mongodb/3.6/",
        "4.0": "https://docs.percona.com/percona-server-for-mongodb/4.0/",
        "4.2": "https://docs.percona.com/percona-server-for-mongodb/4.2/",
        "4.4": "https://docs.percona.com/percona-server-for-mongodb/4.4/",
        "5.0": "https://docs.percona.com/percona-server-for-mongodb/5.0/",
        "Latest stable": "https://docs.percona.com/percona-server-for-mongodb/4.4/"
    },
}
html_logo = '../_static/images/percona-logo.svg'
html_favicon = '../_static/images/percona_favicon.ico'
pygments_style = 'emacs'
gitstamp_fmt = "%b %d, %Y"
# Specify the text pattern that won't be copied with the code block contents
copybutton_prompt_text = '$'
# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_static/_templates/theme']
# Path to custom css files. These will override the default css attribute if they exist
html_css_files = [
    '../_static/css/material.css',
]
