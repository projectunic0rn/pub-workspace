# Discord App

## Summary

Project Unicorn discord workspace app written with Python on Flask and [discord.py](https://discordpy.readthedocs.io/en/latest/api.html) client library, supported by mysql data store.

## Development Dependencies

- [Python 3.x.x](https://www.python.org/downloads/)
- [Docker Engine 19.03.0+](https://docs.docker.com/desktop/#download-and-install)

## Docker Development

[Create a test app](https://discord.com/developers/applications). Once created, copy/paste the [docker-compose.env.example](../../../ci/docker-compose.env.example) 
and rename the new file to `docker-compose.env` (removing .example). Then change the variables to your own application properties.

```bash
# from repo root
# docker compose up
$ docker-compose --file ci/docker-compose.yml up -d

# run alembic migrations to setup db
$ docker exec -it pub-discord-workspace-bot python3 -m alembic.config -c src/persistence/migrations/alembic.ini upgrade head

# find install link, and install app to a test workspace
$ open http://localhost:8002/info

# rebuild images on changes
$ docker-compose --file ci/docker-compose.yml build

# when done
$ docker-compose --file ci/docker-compose.yml down
```

---
**NOTES**

- You can use mysql cli or [mysql workbench](https://www.mysql.com/products/workbench/) to interface with docker instance of mysql.
- More info on managing db migrations found in [persistence readme](../../persistence)

---


## Linting

[Guide](https://docs.pylint.org/en/1.6.0/tutorial.html) to pylint.

```bash
# Run linter
$ python3 -m pylint src --ignore=tests
```

## Testing

```bash
# Run tests
$ pytest
```

Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.
