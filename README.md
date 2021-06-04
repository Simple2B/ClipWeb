# ClipWeb Launch Server Instruction

This is instruction for launch **ClipWeb** server.

**Requirements:**

- Docker
- Docker-Compose

## Deploy from github

Choice folder for deploy E.g.: ~/Clipweb/

Project Clipweb placed in GitHub repository [here](https://github.com/Simple2B/ClipWeb).
Let's download the project from GitHub:

```
git clone https://github.com/Simple2B/ClipWeb.git .
```

## Environment variable

Create .env file like example **sample.env**
Configure for yours settings

## Docker

```bash
docker-compose build
```

```bash
docker-compose up -d
```

## Database

After you defined all your models, Tortoise needs you to init them, in order to create backward relations between models and match your db client with appropriate models.

```python
def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
```
Here we create connection to database client and then we discover & initialize models.

When the app is running a method **init_db** is called.
It registers models at the DB and creates or adds tables to DB
if they do not exist.
