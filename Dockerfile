#pull official base image 
FROM python:3.7.4-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

#set working directory
WORKDIR /usr/src/app

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

#add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

#add app 
COPY . /usr/src/app

#run server
CMD python manage.py run -h 0.0.0.0