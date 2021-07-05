FROM python:3.9.5-slim-buster

WORKDIR /app
ADD . /app

ENV ACCEPT_EULA=Y

RUN apt-get --assume-yes update && \
    apt-get install -y git gcc graphviz &&\
    apt-get install --assume-yes --reinstall build-essential

RUN pip install -r requirements.txt