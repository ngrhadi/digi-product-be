# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
  apt-get install -y gcc libpq-dev && \
  apt-get clean

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the Django project
COPY . .

# Run any necessary commands, like migrations or SQL scripts
RUN poetry run python manage.py runsql /app/sql/master_product.sql
RUN poetry run python manage.py migrate

# Expose the port
EXPOSE 8800

# Run the Django development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8800"]
