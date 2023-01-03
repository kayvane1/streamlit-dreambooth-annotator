# streamlit-dreambooth-annotator

Small Streamlit app to label datasets to use in Dreambooth using HuggingFace

## Setup

This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Setup has been simplified with a Makefile. To setup the project, run:

```bash
make init
```

This will create a virtual environment and install all dependencies as well as set-up the pre-commit hooks.

To start the app, run:

```bash
poetry run streamlit run app.py
```

## Developing

Check the [CONTRIBUTING.md](/CONTRIBUTING.md) for information about how to develop on this project.
