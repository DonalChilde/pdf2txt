"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from importlib.metadata import distribution

sys.path.insert(0, os.path.abspath("../../src"))
import pdf2txt  # pylint: disable=wrong-import-position

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
distro = distribution("pdf2txt")
project = distro.metadata["Name"]
project_copyright = f"2024, {distro.metadata['Author']}"
author = distro.metadata["Author"]
# The full version, including alpha/beta/rc tags.
release = distro.metadata["Version"]
# The short X.Y.Z version.
version = release


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_click",
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []

# Mapping Example
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3", None),
#     "aiohttp_queue": ("https://pfmsoft-aiohttp-queue.readthedocs.io/en/latest/", None),
# }
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
