FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y -qq install net-tools

RUN \
apt-get update && \
apt-get -y -qq upgrade && \
apt-get -y -qq install net-tools && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

WORKDIR /code

ADD requirements.txt /code

RUN pip3 install -r requirements.txt

ADD . /code
