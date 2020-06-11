# Discord App
## Summary 
Project Unicorn discord workspace app written with Python on Flask and discord.py client library.

## Development Dependencies
- [Python 3.x.x](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/desktop/#download-and-install)

## Quick Start
```bash
# navigate to directory
$ cd src/apps/discord

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
$ docker build -t pub-discord-workspace -f ci/discordworkspace.Dockerfile src/apps/discord
# run container
$ docker run -d --name pub-discord-workspace -p 80:80 -e DISCORD_BOT_TOKEN=yourlocaldiscordbottoken pub-discord-workspace
# Direct browser to localhost port 80
$ open http://localhost:80
# Stop and remove container
$ docker rm -f pub-discord-workspace
```

## Linting
[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint.

```bash
# Run linter
$ python3 -m pylint src --ignore=tests
```

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.

