# PHDI Transforms Library

## Development

### Installing

This library uses [Poetry](https://python-poetry.org/) to manage dependencies. To get started
run `poetry install`. After the dependencies are installed, you can either run `poetry shell` to
activate poetry's virtualenv or `poetry run $YOUR_COMMAND` to run single commands within the virtualenv.
To run the tests (and black, and flake8), this would be `poetry run make test`.

### Building the docs

We're using [Sphinx](https://www.sphinx-doc.org) to write up external docs, but there's a Make target
to help out. Running `make docs` should build a single html file in `docs/_build/singlehtml/index.html`.
