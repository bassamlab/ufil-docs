# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Unified Framework for Infrastructure Localization'
copyright = '2026 Cyber-Physical Mobility Group'
author = 'Cyber-Physical Mobility Group'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme', 'sphinx_copybutton', 'sphinxcontrib.mermaid']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
#html_theme = "pydata_sphinx_theme"
#html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

# -- Mermaid diagrams (same setup as the CPM Lab documentation) ---------------
# The diagrams are rendered in the browser; Mermaid and the ELK layout engine are loaded from
# cdn.jsdelivr.net. ELK must be included explicitly, otherwise "layout": "elk" falls back to dagre.
mermaid_version = "12.0.0"
mermaid_output_format = "raw"
mermaid_include_elk = True
mermaid_elk_version = "1.0.2"  # first layout-elk release for Mermaid 12

mermaid_dark_theme = "redux"
mermaid_light_theme = "redux"

mermaid_config = {
    "startOnLoad": False,
    "layout": "elk",
}
