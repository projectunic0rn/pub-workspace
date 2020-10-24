# Persistence
Database tables correspond to a *_entity.py class. To add, remove, or modify a table you can create, delete, or update the corresponding *_entity.py file. Database versioning is managed with alembic. Alembic commands depend on the presence of the database connection string via `os.environ["WORKSPACES_CONNECTION_STRING"]`.

## Migration Commands
```bash
# from repo root
# create new migration
$ python3 -m alembic.config -c src/persistence/migrations/alembic.ini revision --autogenerate -m "comment for revision"

# update database
$ python3 -m alembic.config -c src/persistence/migrations/alembic.ini upgrade head

```

---
**NOTES**

- [alembic documentation](https://alembic.sqlalchemy.org/en/latest/)

---