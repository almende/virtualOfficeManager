# pull official base image
FROM python:3.6.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy app code
COPY ./flaskr ./flaskr
COPY ./manage.py .

# copy google service files
COPY ./google_service_account/ ./google_service_account
