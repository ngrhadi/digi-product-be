poetry config virtualenvs.in-project true
poetry install --no-root
poetry shell
poetry env use 3.8.12

