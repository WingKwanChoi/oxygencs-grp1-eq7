FROM python:3.8-alpine

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# App specific environnement variables.
ENV HOST=http://159.203.50.162
ENV TOKEN=999109532408abf795f3
ENV T_MAX=25
ENV T_MIN=18
ENV DATABASE_URL='postgresql://user01eq7:nJCxUQQGEzAYKnWw@157.230.69.113/db01eq7'

WORKDIR /app

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Install the application's dependencies.
# Install dependecies
RUN pip install tomli --user
RUN pip install pipenv --user
RUN python -m pipenv install

# Run the application.
CMD python -m pipenv run start