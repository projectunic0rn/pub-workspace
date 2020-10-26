# Persistence
Database tables correspond to a *_entity.py class. To add, remove, or modify a table you can create, delete, or update the corresponding *_entity.py file. Database versioning is managed with alembic.

## Migration Commands

```bash
# from repo root
# create new migration
$ docker exec -it pub-discord-workspace-bot python3 -m alembic.config -c src/persistence/migrations/alembic.ini revision --autogenerate -m "comment for revision"

# update database
$ docker exec -it pub-discord-workspace-bot python3 -m alembic.config -c src/persistence/migrations/alembic.ini upgrade head

```

---
**NOTES**

- [alembic documentation](https://alembic.sqlalchemy.org/en/latest/)

---