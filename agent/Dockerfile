FROM python:3

MAINTAINER Christian Jensen <christian@jensenbox.com>

ENV PYTHONUNBUFFERED 1
ENV SN_AGENT_ID b545478a-971a-48ec-bc56-4b9b7176799c
ENV SN_SERVICE_ADAPTER_CONFIG_FILE service_adapter_config_example.yml
WORKDIR /develop
ADD requirements.txt /develop
RUN pip install -r requirements.txt
