ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-alpine as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Step 2: Set environment variables for Poetry
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \ 
    # Tell Docker not to install the pakage in an environemnt, Docker it self is an environment
    POETRY_VIRTUALENVS_CREATE=false \ 
    PIP_NO_CACHE_DIR=off

# Install Poetry 
RUN pip install poetry

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"


WORKDIR /app

# Copy the project files (including pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock /app/


# Install dependencies with Poetry
RUN poetry install --no-root

# Copy the source code into the container.
COPY . /app


# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0" , "--port", "8000"]
