# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GADMA Workshops'
copyright = '2024, Ekaterina Noskova'
author = 'Ekaterina Noskova'
#release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

def setup(app):
    app.add_css_file('styles.css')

extensions = [
    "myst_parser",
    "sphinx_inline_tabs",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = []

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution"
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ["_static"]
html_css_files = [
    'css/bootstrap_namespaced.css',
]
html_theme_options = {
    "source_repository": "https://github.com/noscode/GADMA_workshops",
    "source_branch": "master",
    "source_directory": "docs/",
}
