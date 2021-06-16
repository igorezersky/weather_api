# base image
FROM python:3.9-buster

# add service user
ARG PROJECT_USER
RUN adduser --disabled-password ${PROJECT_USER}
WORKDIR /home/${PROJECT_USER}

USER ${PROJECT_USER}

# create project dir
RUN mkdir weather_api
WORKDIR /home/${PROJECT_USER}/weather_api
RUN mkdir logs

# install requirements
COPY *.txt ./
ARG VIRTUAL_ENV
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# copy project files
COPY LICENSE *.py *.in ./
COPY weather_api weather_api
