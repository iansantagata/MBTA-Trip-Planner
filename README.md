# MBTA Wrapper

This project is an example project which utilizes the Massachusetts Bay Transit Authority's (MBTA's) API to answer questions about train transit around the Boston area.

See [docs/] for more description on each question addressed by this application.

## Quick Start

You will need [python](https://www.python.org/downloads/) or an equivalent Python environment manager (e.g. [pyenv](https://github.com/pyenv/pyenv)) installed on your machine.

Run the following commands at the top level of the repository:

```bash
# Create a virtual environment named ".venv"
python -m venv .venv

# Activate the virtual environment based on OS
source .venv/Scripts/activate  # For Windows
source .venv/bin/activate      # For MacOS / Linux

# Install project dependencies to the virtual environment
pip install -e .       # Installs application dependencies only
pip install -e .[dev]  # Installs application dependencies plus local development dependencies
```

## Quick Clean Up

Run the following commands at the top level of the repository:

```bash
# Exit the virtual environment
deactivate

# Delete the virtual environment named ".venv"
rm -rf .venv/
```

## Local Development

Ensure that local development dependencies have been installed in the quick start guide (above) before continuing.

To format, lint, and type check code in this repository, run any of the following commands at repository root:

```bash
# Sort imports
isort .

# Format code
black .

# Lint code
pylint .

# Static type check
mypy .
```

To test code in this repository, run `pytest` at repository root.
