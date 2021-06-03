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
