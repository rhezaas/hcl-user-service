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

## start main.py
ENTRYPOINT ["python3", "app/main.py"]

## expose port 8081
EXPOSE 8081