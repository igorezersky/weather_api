# weather_api

## Overview

This is a RESTful and asynchronous (created via [igorezersky/cookiecutter-api](https://github.com/igorezersky/cookiecutter-api)) weather API, created as a pet project to demonstrate my skills in API development.

## Requirements

Please visit openweathermap.org and sign in\up to receive an API key.

### Docker

Normally, to build project image you will need to install following packages:

- [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)

- [pydeployhelp](https://pypi.org/project/pydeployhelp/)

## Installation

### Linux | Windows | macOS

Following instructions are guidelines, you can install it differently, however,
executing the following commands will ensure that `weather_api` is installed correctly:

Clone repository and create [virtual environment](https://docs.python.org/3/library/venv.html):

```console
foo@bar:~$ git clone https://github.com/igorezersky/weather_api && cd weather_api
foo@bar:~/weather_api python -m venv venv && source venv/bin/activate
foo@bar:~/weather_api python -m pip install --upgrade pip wheel setuptools
```

Install requirements:

```console
foo@bar:~/weather_api pip install -r requirements.txt
```

### Docker

Make sure that you have execution permissions for `docker`, `docker-compose` and `python`.

Use `pydeployhelp` package to build project image:

```console
foo@bar:~/weather_api pydeployhelp
Enter deploy tasks from following: all | build up down: build
        ✓ processing deploy tasks: build
Enter deploy targets from following: all | weather_api: all
        ✓ processing deploy targets: weather_api
Do you agree to start processing (yes or no)? [yes]: yes
```

## Usage

Create `.env` file with following variables:

```text
ENV=dev
PROJECT_NAME=weatherapi
HOST=localhost
PORT=8888
ENABLE_CORS=True
API_KEY=key from openweathermap.org
VOLUMES_ROOT=/$HOME/projects/weather_api
```

### Linux | Windows | macOS

You can manually start project:

```console
foo@bar:~/weather_api uvicorn run:server --port 8000 --host 0.0.0.0 --proxy-headers --forwarded-allow-ips '*'
```

### Docker

Use `pydeployhelp` package to run project image:

```console
foo@bar:~/weather_api pydeployhelp
Enter deploy tasks from following: all | build up down: up
        ✓ processing deploy tasks: up
Enter deploy targets from following: all | weather_api: all
        ✓ processing deploy targets: weather_api
Do you agree to start processing (yes or no)? [yes]: yes
```
