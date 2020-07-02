# pull official base image
FROM python:3.6.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy files
COPY ./setup.py ./setup.py
COPY ./flaskr ./flaskr
COPY ./instance ./instance

# install code and dependencies
RUN pip install --upgrade pip
RUN pip install -e .
