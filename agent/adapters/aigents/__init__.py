#
# agent/adapters/aigents/__init__.py - adapter integrating different sub-services of Aigents web service,
# such as RSS feeding, social graph discovery, summarizing text extraction by pattern and entity attribution
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import urllib.parse
from typing import List

import requests
import json
import feedparser

from adapters.aigents.settings import AigentsSettings
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)


class AigentsAdapter(ServiceAdapterABC):
    type_name = "AigentsAdapter"

    def __init__(self, app, service: Service, required_services: List[Service]) -> None:
        super().__init__(app, service, required_services)

        self.settings = AigentsSettings()

    def post_load_initialize(self, service_manager: ServiceManager):
        super().post_load_initialize(service_manager)

        # TODO login to Aigents here to work in one session? But then need to RSS working even if session is active and handle expired sessions as well!
        pass

    def get_attached_job_data(self, job_item: dict) -> dict:

        # Make sure the input type is one we can handle...
        input_type = job_item['input_type']
        if input_type != 'attached':
            logger.error("BAD input dict %s", str(job_item))
            raise RuntimeError("Aigents - job item 'input_type' must be 'attached'.")

        # Pull the input data from the job item
        input_data = job_item['input_data']
        if input_data is None:
            raise RuntimeError("Agients - job item 'input_data' must be defined.")

        return input_data

    def request(self, session, request):
        url = self.settings.AIGENTS_PATH + "?" + request
        logger.info(url)
        r = session.post(url)
        if r is None or r.status_code != 200:
            raise RuntimeError("Aigents - no response")
        logger.info(r.text)
        return r

    def validate(self, data, key):
        if not key in data or len(data[key]) < 1:
            raise RuntimeError("Aigents - no input data " + key)
        return data[key]

    def create_session(self):
        session = requests.session()
        # TODO login in one query, if/when possible
        url = self.settings.AIGENTS_PATH + "?my email " + self.settings.AIGENTS_LOGIN_EMAIL + "."
        logger.info(url)
        r = session.post(url);
        logger.info(r.text)
        url = self.settings.AIGENTS_PATH + "?" + urllib.parse.quote_plus(
            "my " + self.settings.AIGENTS_SECRET_QUESTION + " " + self.settings.AIGENTS_SECRET_ANSWER + ".")
        logger.info(url)
        r = session.post(url)
        logger.info(r.text)
        # set language
        url = self.settings.AIGENTS_PATH + "?my language english."
        logger.info(url)
        r = session.post(url);
        logger.info(r.text)
        return session

    def perform(self, job: JobDescriptor):
        logger.debug("Performing Aigents job.")

        # Process the items in the job. The job may include many
        results = []
        for job_item in job:

            # Get the input data for this job.
            job_data = self.get_attached_job_data(job_item)
            logger.info(job_data)

            if not 'data' in job_data:
                raise RuntimeError("Aigents - no input data")

            r, parsed_text = self.aigents_perform(job_data['data'])
            if r is None or r.status_code != 200:
                raise RuntimeError("Aigents - no response")

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'adapter_type': 'aigents',
                'service_type': job_data["type"],
                # TODO cleanup, based on service request and response ontology discussion?
                'response_data': parsed_text
            }
            results.append(single_job_result)

        # Return the list of results that come from appending the results for the
        # individual job items in the job.
        return results

    # Placeholder or virtual method for child override
    def aigents_perform(self, data):
        return None, None


class AigentsTextsClustererAdapter(AigentsAdapter):
    type_name = "AigentsTextsClustererAdapter"

    def example_job(self):
        return [
            {
                "input_type": "attached",
                "input_data": {
                    "type": "texts_cluster",
                    "data": {
                        "texts": [
                            "http://aigents.com/test/cat/fly.html",
                            "http://aigents.com/test/cat/eagle.html",
                            "http://aigents.com/test/cat/snake.html",
                            "tuna is a fish",
                            "cat is a mammal",
                            "http://aigents.com/test/cat/french.html",
                            "http://aigents.com/test/cat/chinese.html",
                            "germans live in germany",
                            "russians live in russia",
                            "spaniards live in spain"
                        ]
                    }
                },
                "output_type": "attached"
            }
        ]

    def aigents_perform(self, data):
        texts = self.validate(data, "texts")
        texts_as_string = json.dumps(texts)
        request_text = "You cluster format json texts '%s'!" % texts_as_string
        s = self.create_session()
        r = self.request(s, request_text)
        parsed_text = json.loads(r.text)
        return r, parsed_text


class AigentsTextExtractorAdapter(AigentsAdapter):
    type_name = "AigentsTextExtractorAdapter"

    def example_job(self):
        return [
            {
                "input_type": "attached",
                "input_data": {"type": "text_extract", "data": {
                    "pattern": "{president presidency presidents presidential}",
                    "text": 'Yo! Washington was first president of the United States. Also, can place url here: https://www.nytimes.com/'
                }},
                "output_type": "attached"
            }
        ]

    def aigents_perform(self, data):
        pattern = self.validate(data, "pattern")
        text = self.validate(data, "text")
        s = self.create_session()
        # TODO cleanup and streamline, make json in http header 'Accept': 'application/json'
        # specify format
        self.request(s, "peer has format.")
        self.request(s, "my format json.")
        # set user context
        self.request(s, "my knows '" + pattern + "', trusts '" + pattern + "'.")
        self.request(s, "my sites '" + pattern + "', trusts '" + text + "'.")
        self.request(s, "is '" + pattern + "' new false.")
        self.request(s, "no there is '" + pattern + "'.")
        # do extraction and request data
        self.request(s, "You reading '" + pattern + "' in '" + text + "'!")
        r = self.request(s, "what is '" + pattern + "' text, about, context?")
        # clear user context
        self.request(s, "my knows no '" + pattern + "', trusts no '" + pattern + "'.")
        self.request(s, "my sites no '" + pattern + "', trusts no '" + text + "'.")
        self.request(s, "my format not json.")
        parsed_text = json.loads(r.text)
        return r, parsed_text


class AigentsRSSFeederAdapter(AigentsAdapter):
    type_name = "AigentsRSSFeederAdapter"

    def example_job(self):
        return [
            {
                "input_type": "attached",
                "input_data": {"type": "rss_feed", "data": {
                    "area": 'ai'
                }},
                "output_type": "attached"
            },
            {
                "input_type": "attached",
                "input_data": {"type": "rss_feed", "data": {
                    "area": 'business'
                }},
                "output_type": "attached"
            }
        ]

    def aigents_perform(self, data):
        area = self.validate(data, "area")
        # sessionless request
        r = requests.post(self.settings.AIGENTS_PATH + "?rss%20" + area)
        logger.info(r)
        parsed_text = feedparser.parse(r.text)
        return r, parsed_text


class AigentsSocialGrapherAdapter(AigentsAdapter):
    type_name = "AigentsSocialGrapherAdapter"

    def example_job(self):
        return [
            {
                "input_type": "attached",
                "input_data": {
                    "type": "social_graph",
                    "data": {
                        'network': 'steemit',
                        'userid': 'aigents',
                        'period': "180"}
                },
                "output_type": "attached"
            },
            {
                "input_type": "attached",
                "input_data": {
                    "type": "social_graph",
                    "data": {
                        'network': 'golos',
                        'userid': 'aigents',
                        'period': "180"}
                },
                "output_type": "attached"
            }
        ]

    def aigents_perform(self, data):
        network = self.validate(data, "network")
        userid = self.validate(data, "userid")
        days = self.validate(data, "period")
        s = self.create_session()
        url = self.settings.AIGENTS_PATH + "?" + network + ' id ' + userid + ' report, period ' + days + ', format json, authorities, fans, similar to me'
        r = self.request(s, url)
        parsed_text = json.loads(r.text)
        return r, parsed_text
