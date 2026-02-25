# Foundation Models SDK for Python Documentation

This directory contains the Sphinx documentation for the Foundation Models SDK for Python.

## Building the Documentation

### Prerequisites

Install documentation dependencies using `uv`:

```bash
uv sync --group docs
```

Alternatively, if you prefer using `pip`:

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `build/html/`. Open `build/html/index.html` in your browser to view it.

### Clean Build Files

```bash
cd docs
make clean
```

## Writing Documentation

### reStructuredText Basics

- Use `.rst` extension for documentation files
- Headers use underlines: `=` for titles, `-` for sections, `~` for subsections
- Code blocks use `.. code-block:: python` directive
- Cross-references use `:doc:` and `:ref:` roles

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory
2. Add it to the `toctree` in the parent document
3. Build and verify the documentation

### Code Examples

Include code examples using:

```rst
.. code-block:: python

   import apple_fm_sdk as fm

   model = fm.SystemLanguageModel()
```

### API Documentation

API documentation is auto-generated from docstrings using:

```rst
.. autoclass:: apple_fm_sdk.ClassName
   :members:
   :undoc-members:
   :show-inheritance:
```

## GitHub Pages Deployment

Run the script `bash ./bin/publish-docs.sh`.

## Local Development

For rapid iteration during development:

```bash
# Install sphinx-autobuild using uv
uv pip install sphinx-autobuild

# Or add to pyproject.toml docs group and run:
# uv sync --group docs

# Run auto-rebuilding server
cd docs
sphinx-autobuild source build/html
```

The documentation will automatically rebuild when you save changes.

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Check that all required packages are installed
2. Verify that all `.rst` files have valid syntax
3. Ensure all cross-references point to existing documents
4. Check that code examples are properly formatted

### Missing Modules

If autodoc can't find modules:

1. Ensure the package is installed: `uv pip install -e .` (or `pip install -e .`)
2. Check that the module path is correct in `conf.py`
3. Verify that `__init__.py` files exist in all package directories

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)

---
For licensing see accompanying LICENSE file.
Copyright (C) 2026 Apple Inc. All Rights Reserved.


