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

```bash
# build docker image
$ docker build -t pub-slack-workspace -f ci/slackworkspace.Dockerfile .

# run container
$ docker run -d --name pub-slack-workspace -p 5001:80 -e SLACK_SIGNING_SECRET=signing_secret -e WORKSPACES_CONNECTION_STRING=connection_string DISCORD_BOT_TOKEN=yourlocaldiscordbottoken -e SLACK_SIGNING_SECRET=signing_secret -e SLACK_CLIENT_SECRET=client_secret -e SLACK_REDIRECT_URI=redirect_uri -e APP_URL=https://projectunicorn.net -e APP_ENV=development pub-slack-workspace

# Direct browser to localhost port 5000
$ open http://localhost:5000

# Stop and remove container
$ docker rm -f pub-slack-workspace
```

## Linting
[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint. 

```bash
# Run linter
$ python3 -m pylint src --ignore=tests
```

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.

