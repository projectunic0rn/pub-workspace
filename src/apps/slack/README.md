# Slack App
## Summary 
Project Unicorn slack workspace app written with Python on Flask.

## Development Dependencies
- [Python 3.x.x](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/desktop/#download-and-install)

## Quick Start
```bash
# navigate to slack directory
$ cd src/slack

# Install dependencies
$ pip3 install -r requirements.txt

# Run development server
$ export FLASK_APP=app.py
$ python3 -m flask run

# Run linter
$ cd src
$ python3 -m pylint slack

# Run tests
$ pytest

# If new dependency installed, update requirements.txt
$ pip3 freeze > requirements.txt
```

## Docker Development

```bash
# build docker image
$ docker build -t pub-slack-workspace -f ci/slackworkspace.Dockerfile src/slack
# run container
$ docker run -d --name pub-slack-workspace -p 80:80 -e SLACK_SIGNING_SECRET=yourlocalslacksecret pub-slack-workspace
# Direct browser to localhost port 80
$ open http://localhost:80
# Stop and remove container
$ docker rm -f pub-slack-workspace
```

## Linting
[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint. 

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.

