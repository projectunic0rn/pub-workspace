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

### Web Service
```bash
# build docker image
$ docker build -t pub-slack-workspace -f ci/slackworkspace.Dockerfile .

# run container (provide your environment variables), service bus must be test instance running on azure
$ docker run -d --name pub-slack-workspace -p 5001:80 -e SLACK_SIGNING_SECRET=signing_secret -e SLACK_CLIENT_ID=client_id -e SLACK_CLIENT_SECRET=client_secret -e SLACK_REDIRECT_URI=redirect_uri -e APP_URL=https://projectunicorn.net -e APP_ENV=development -e SERVICE_BUS_CONN_STR=bus_connection_string -e SERVICE_BUS_QUEUE_NAME=queue_name pub-slack-workspace 

# Confirm running by visitng 
$ open http://localhost:5001/info

# Stop and remove container
$ docker rm -f pub-slack-workspace
```

### Slack App
```bash
# build docker image
$ docker build -t pub-slack-workspace-bot -f ci/slackworkspacebot.Dockerfile .

# run container (provide your environment variables), service bus must be test instance running on azure
$ docker run -d --name pub-slack-workspace-bot -e WORKSPACES_CONNECTION_STRING=connection_string DISCORD_BOT_TOKEN=yourlocaldiscordbottoken -e APP_URL=https://projectunicorn.net -e APP_ENV=development -e SERVICE_BUS_CONN_STR=bus_connection_string -e SERVICE_BUS_QUEUE_NAME=queue_name pub-slack-workspace-bot

# Stop and remove container
$ docker rm -f pub-slack-workspace-bot
```

## Linting
[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint. 

```bash
# Run linter
$ python3 -m pylint src --ignore=tests
```

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.

