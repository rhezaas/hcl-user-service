## define python ver
FROM python:3

## i write this :v
MAINTAINER Rheza

## working directory
WORKDIR /usr/src

## copy app folder to 
COPY app app

## copy requeiremtns.txt to workdir
COPY requirements.txt requirements.txt

## copy dotenv
COPY .env .env

## install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app/main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_RUN_PORT=8081
ENV FLASK_RUN_HOST=0.0.0.0

## start main.py
ENTRYPOINT ["flask", "run"]

## expose port 8081
EXPOSE 8081