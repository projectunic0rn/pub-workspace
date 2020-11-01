# Slack App
## Summary 
Project Unicorn slack workspace app written with Python on Flask.

## Development Dependencies
- [Python 3.x.x](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/desktop/#download-and-install)

## Quick Start
```bash
# navigate to directory
$ cd src/apps/slack

# Install dependencies
$ pip3 install -r requirements.txt

# Run development server
$ export FLASK_APP=app.py
$ python3 -m flask run

# Run tests
$ pytest

# If new dependency installed, update requirements.txt
$ pip3 freeze > requirements.txt
```

## Docker Development

[Create a test app](https://api.slack.com/apps). Once created, copy/paste the [docker-compose.env.example](../../../ci/docker-compose.env.example) 
and rename the new file to `docker-compose.env` (removing .example). Then change the variables to your own application properties.

```bash
# from repo root
# docker compose up
$ docker-compose --file ci/docker-compose.yml up -d

# run alembic migrations to setup db
$ docker exec -it pub-slack-workspace-bot python3 -m alembic.config -c src/persistence/migrations/alembic.ini upgrade head

# view app install link via flask app ui
# app should be installed through a project page via pub ui https://github.com/projectunic0rn/pub
# installing the app directly is untested and may cause errors
$ open http://localhost:8003/info

# rebuild images on changes
$ docker-compose --file ci/docker-compose.yml build

# when done
$ docker-compose --file ci/docker-compose.yml down
```

## Linting
[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint. 

```bash
# Run linter
$ python3 -m pylint src --ignore=tests
```

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.

