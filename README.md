# Speaq-AI API

## Setup

1. Clone this repository onto your local machine: `git clone https://github.com/speaq-ai/api.git`.
2. Install Docker if you don't already have it. [Docker docs](https://docs.docker.com/install/)
3. Create an `env` directory. Inside of that directory, create two files: `api_dev.env` and `postgres_dev.env`.
4. Inside of `api_dev.env`, add the following variables, with the values I provided:

```
DB_PASSWORD=<your-db-password>
DB_USER=<your-db-username>
DB_NAME=<your-db-name>
DB_HOST=<your-db-host>
DB_PORT=<your-port>
```

5. Inside of `postgres_dev.env`, add the following variables, with the values I provided:

```
POSTGRES_PASSWORD=<your-db-password>
POSTGRES_USER=<your-db-user>
POSTGRES_DB=<your-db-name>
```

6. Start the docker containers and create a django superuser with: `docker-compose up -d && docker exec -it speaq-api python manage.py createsuperuser`. Follow the prompts to create the super user.

7. Finally, restart the docker containers: `docker-compose down && docker-compose up`.

8. You're all set! Go to `localhost:8000/admin` and log in with the superuser credentials you supplied earlier.

## Usage

Start the Docker containers with `docker-compose up`

Once the containers are running, you can access the API's admin dashboard at `localhost:8000/admin`.

## Configuration Steps

These are the components I've included steps I took to configure them for this project. No need understand everything going on here, but I wanted to give a high-level overview for reference.

### Components

- Django
- Postgres
- Docker

### Steps:

- create venv
- install django, djangorestframework, psycopg
- freeze requirements to a `requirements.txt` file
- use `django-admin` to create project and needed apps inside of `src` directory.
- set up `Dockerfile` and `docker-compose.yaml`
- configure django database settings to use postgres engine
- use manage.py to run initial migration
- once docker network is up and running, use manage.py to create super user inside container.

### Additional optimizations:

- include the `./src` directory as a docker volume in API service to enable hot reloads.
