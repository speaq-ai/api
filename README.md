# Speaq-AI API

## Setup

1. Clone this repository onto your local machine: `git clone https://github.com/speaq-ai/mockup.git`.
2. Install yarn: `brew install yarn` on Mac, for other OS see [docs](https://yarnpkg.com/lang/en/docs/install/#mac-stable).
3. Install dependencies: `yarn install`.
4. create a `.env` file in the root directory of this project. Set the following environment variables with appropriate values.

```
MAPBOX_ACCESS_TOKEN=<your-mapbox-token>
```

## Usage

To start the development web server: `yarn start`

Once the development web server is running, you can view the app at `localhost:8080`.

## Configuration Steps

These are the components I've included steps I took to configure them for this project. No need understand everything going on here, but I wanted to give a high-level overview for reference.

### Components

- Django: package manager (variant of npm that was created by Facebook)

### Steps:

- create venv
- install django, djangorestframework, psycopg
- freeze requirements to a `requirements.txt` file
- use `django-admin` to create project and needed apps inside of `src` directory.
- set up `Dockerfile` and `docker-compose.yaml`
- configure django database settings to use postgres engine
- use manage.py to run initial migration
- once docker network is up and running, use manage.py to create super user inside container.

[Reference](https://dev.to/nsebhastian/step-by-step-react-configuration-2nma#why-create-your-own-configuration)
