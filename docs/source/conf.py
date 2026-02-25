# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root to the path so we can import the package
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Foundation Models SDK for Python"
copyright = "2026, Apple Inc"
author = "Apple Inc."
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "myst_parser",
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = False

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "private-members": False,  # Exclude private members (starting with _)
    "show-inheritance": False,  # Don't show inheritance to hide base classes
}
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_class_signature = "separated"  # Show class signature separately from bases

# Generate TOC entries for autodoc objects (methods, functions, etc.)
toc_object_entries = True
toc_object_entries_show_parents = "hide"


# Custom function to skip private parameters and base classes
def skip_private_members(app, what, name, obj, skip, options):
    """Skip private members, _ptr parameters, and _ManagedObject inheritance."""
    # Skip any member that starts with underscore
    if name.startswith("_"):
        return True
    return skip


def process_signature(app, what, name, obj, options, signature, return_annotation):
    """Remove _ptr parameter from signatures."""
    if signature and "_ptr" in signature:
        # Remove _ptr parameter from signature
        import re

        # Match _ptr parameter with optional type annotation and default value
        # Handle various formats: _ptr=None, _ptr: type = None, _ptr: type, _ptr
        signature = re.sub(r",\s*_ptr\s*:\s*[^,)=]*\s*=\s*[^,)]*", "", signature)
        signature = re.sub(r",\s*_ptr\s*=\s*[^,)]*", "", signature)
        signature = re.sub(r",\s*_ptr\s*:\s*[^,)]*", "", signature)
        signature = re.sub(r",\s*_ptr", "", signature)
        # Also handle if _ptr is the first parameter (unlikely but possible)
        signature = re.sub(r"\(_ptr\s*:\s*[^,)=]*\s*=\s*[^,)]*,\s*", "(", signature)
        signature = re.sub(r"\(_ptr\s*=\s*[^,)]*,\s*", "(", signature)
        signature = re.sub(r"\(_ptr\s*:\s*[^,)]*,\s*", "(", signature)
        signature = re.sub(r"\(_ptr,\s*", "(", signature)
    return (signature, return_annotation)


def setup(app):
    """Setup function for Sphinx extension."""
    app.connect("autodoc-skip-member", skip_private_members)
    app.connect("autodoc-process-signature", process_signature)


# MyST Parser settings (for Markdown support)
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "smartquotes",
]

# MyST heading anchors and url schemes
myst_heading_anchors = 4
myst_url_schemes = ["http", "https", "mailto", "ftp", "phantom", "adir"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_title = "Foundation Models SDK for Python"
html_short_title = "Foundation Models SDK for Python"
html_logo = "_static/foundation-models-framework-logo.png"
html_favicon = "_static/foundation-models-framework-logo.png"
html_static_path = ["_static"]

# Sphinx Book Theme options (matching CoreML Tools)
html_theme_options = {
    "repository_url": "https://github.com/apple/python-apple-fm-sdk",
    "use_repository_button": True,
    "show_toc_level": 3,  # Show deeper TOC levels in right sidebar
}

# Add any paths that contain custom static files (such as style sheets)
html_css_files = [
    "custom.css",
]

# Copybutton configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
