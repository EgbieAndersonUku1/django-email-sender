# conf.py

project = 'django-email-sender'

extensions = [
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}



html_theme = 'furo'

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

suppress_warnings = ["myst.header"]
