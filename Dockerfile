# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
# Allow statements and log messages to immediately appear
 PYTHONUNBUFFERED=1 \
# disable a pip version check to reduce run-time & log-spam
 PIP_DISABLE_PIP_VERSION_CHECK=1 \
# cache is useless in docker image, so disable to reduce image size
 PIP_NO_CACHE_DIR=1


ENV HOST=http://159.203.50.162 \ 
 TOKEN=999109532408abf795f3 \
 T_MAX=25 \
 T_MIN=18 \
 DATABASE_URL='postgresql://user01eq7:nJCxUQQGEzAYKnWw@157.230.69.113/db01eq7'

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Pipfiles
COPY Pipfile Pipfile.lock /app/

# Install pipenv and install dependencies
RUN pip install pipenv 
RUN pipenv install --ignore-pipfile

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . /app

# Run the command to start your application
CMD ["pipenv", "run", "start"]