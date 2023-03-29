FROM python:3.11

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.4.0
ENV PATH=$POETRY_HOME/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

# Make port 8080 available to the world outside this container
EXPOSE 8080

ENV SERVER_ENV="production"

# Run server when the container launches
CMD ["python3", "mancala_frontend/main.py"]
