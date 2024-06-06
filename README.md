### Required
- install [POETRY](https://python-poetry.org/docs/#installation) - Poetry is a tool for dependency management and packaging in Python
- reproduce env file with your configuration database (postgresql)

### Step to reproduce
```bash
# going to inside project and create venv automatically
poetry shell

# install dependencies
poetry install --no-root

# add configuration env in this project
poetry config virtualenvs.in-project true

# then open new terminal and reload windows (using ctrl + shift + P in vscode)
# to make sure all config loaded, and run again
poetry shell

# run migrations
poetry run python manage.py migrate

# create superuser
poetry run python manage.py createsuperuser

# running project
poetry run python manage.py runserver
```
