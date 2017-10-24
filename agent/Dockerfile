FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt /code
RUN pip3 install -r requirements.txt

ADD . /code
