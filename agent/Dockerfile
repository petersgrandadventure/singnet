FROM python:3

MAINTAINER Christian Jensen <christian@jensenbox.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /agent
WORKDIR /agent
ADD . /agent
RUN pip install -r requirements.txt
