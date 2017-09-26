FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /data
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code
