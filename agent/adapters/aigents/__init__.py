#
# agent/adapters/aigents/__init__.py - adapter integrating different sub-services of Aigents web service,
# such as RSS feeding, social graph discovery, summarizing text extraction by pattern and entity attribution
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import urllib.parse
import requests
import logging
from typing import List

from adapters.aigents.settings import AigentsSettings
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC
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

        # Do any agent initialization here.
        # TODO login to Aigents here, but then need to RSS working even if logged and ensure cookie is maintained!?
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

    def request(self,session,request):
        url = self.settings.AIGENTS_PATH+"?"+request
        logger.info(url)
        #TODO use POST
        r = session.get(url)
        if r is None or r.status_code != 200:
            raise RuntimeError("Aigents - no response")
        logger.info(r.text)
        return r

    def create_session(self):
        s = requests.session()
        #TODO use POST
        #TODO login in one query
        url = self.settings.AIGENTS_PATH+"?my email "+self.settings.AIGENTS_LOGIN_EMAIL+"."
        logger.info(url)
        r = s.get(url);
        logger.info(r.text)
        url = self.settings.AIGENTS_PATH+"?"+urllib.parse.quote_plus("my "+self.settings.AIGENTS_SECRET_QUESTION+" "+self.settings.AIGENTS_SECRET_ANSWER+".")
        #url = self.settings.AIGENTS_PATH+"?"+urllib.parse.quote_plus("my email "+self.settings.AIGENTS_LOGIN_EMAIL+", " \
        #        +self.settings.AIGENTS_SECRET_QUESTION+" "+self.settings.AIGENTS_SECRET_ANSWER+", language english.")
        logger.info(url)
        r = s.get(url)
        logger.info(r.text)
        # set language
        url = self.settings.AIGENTS_PATH+"?my language english."
        logger.info(url)
        r = s.get(url);
        logger.info(r.text)
        return s

    def perform(self, job: JobDescriptor):
        logger.debug("Performing Aigents job.")

        # Process the items in the job. The job may include many
        results = []
        for job_item in job:

            # Get the input data for this job.
            #TODO sort out different sub-service adapters
	    #TODO validation
            job_data = self.get_attached_job_data(job_item)
            logger.info(job_data)

            if job_data["type"] == "rss_feed":
                area = job_data["data"]["area"]
                r = requests.get(self.settings.AIGENTS_PATH+"?rss%20"+area)
                logger.info(r)

            if job_data["type"] == "social_graph":
                network = job_data["data"]["network"]
                userid = job_data["data"]["userid"]
                #TODO make configurable
                days = "180"
                s = self.create_session()
                # get data
                url = self.settings.AIGENTS_PATH+"?"+network+' id '+userid+' report, period '+days \
				+', format json, authorities, fans, similar to me'
                logger.info(url)
                r = s.get(url)
                logger.info(r.text)

            if job_data["type"] == "text_extract":
                pattern = job_data["data"]["pattern"]
                text = job_data["data"]["text"]
                s = self.create_session()
                # get data
                #TODO cleanup and streamline
                self.request(s,"peer has format.")
                self.request(s,"my format json.")
                self.request(s,"my knows '"+pattern+"', trusts '"+pattern+"'.")
                self.request(s,"my sites '"+pattern+"', trusts '"+text+"'.")
                self.request(s,"is '"+pattern+"' new false.")
                self.request(s,"no there is '"+pattern+"'.")
                self.request(s,"You reading '"+pattern+"' in '"+text+"'!")
                r = self.request(s,"what is '"+pattern+"' text, about, context?")
                self.request(s,"my knows no '"+pattern+"', trusts no '"+pattern+"'.")
                self.request(s,"my sites no '"+pattern+"', trusts no '"+text+"'.")   
                self.request(s,"my format not json.")

            if job_data["type"] == "texts_cluster":
                texts = job_data["data"]["texts"]
                s = self.create_session()
                r = self.request(s,"You cluster format json texts '"+texts+"'!")

            #TODO cleanup to use .request
            if r is None or r.status_code != 200:
                raise RuntimeError("Aigents - no response")

            output = r.text

            # Add the job results to our combined results array for all job items.
            single_job_result = {
		'adapter_type' : 'aigents',
		'service_type' : job_data["type"], #TODO cleanup?
                'response_data': output
            }
            results.append(single_job_result)

        # Return the list of results that come from appending the results for the
        # individual job items in the job.
        return results


class AigentsClustererAdapter(AigentsAdapter):
    type_name = "AigentsClustererAdapter"



