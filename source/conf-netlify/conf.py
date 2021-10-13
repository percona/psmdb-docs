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
        "3.6": "https://psmdb-docs-36.netlify.app/",
        "4.0": "https://psmdb-docs-40.netlify.app/",
        "4.2": "https://psmdb-docs-42.netlify.app/",
        "4.4": "https://psmdb-docs-44.netlify.app/",
        "5.0": "https://psmdb-docs-50.netlify.app/",
        "Latest": "https://psmdb-docs-50.netlify.app/"
    },
}
html_logo = '../_static/images/percona-logo.svg'
html_favicon = '../_static/images/percona_favicon.ico'
pygments_style = 'emacs'
gitstamp_fmt = "%b %d, %Y"
copybutton_prompt_text = '$'
#html_last_updated_fmt = ''