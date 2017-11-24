#
# agent/adapters/aigents/__init__.py - adapter integrating different sub-services of Aigents web service,
# such as RSS feeding, social graph discovery, summarizing pattern axtraction and entity attribution
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import requests
import logging
from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)


class AigentsAdapter(ServiceAdapterABC):
    type_name = "AigentsAdapter"


    def __init__(self, app, service: Service, required_services: List[Service]) -> None:
        super().__init__(app, service, required_services)

        # Initialize member variables heres.
        self.response_template = None

    def post_load_initialize(self, service_manager: ServiceManager):
        super().post_load_initialize(service_manager)

        # Do any agent initialization here.
        # TODO
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


    def perform(self, job: JobDescriptor):
        logger.debug("Performing Aigents job.")

        # Process the items in the job. The job may include many
        results = []
        for job_item in job:

            # Get the input data for this job.
            #TODO actual parameters handling
            job_data = self.get_attached_job_data(job_item)
            logger.info(job_data)
            #job_params = job_data['params']['job_params']
            #logger.info('Aigents input'+job_params)
            rss_area = job_data['rss_area']

            #TODO config
            r = requests.get("https://aigents.com/al/?rss%20"+rss_area)
            logger.info(r)

            if r is None:
                raise RuntimeError("Aigents - no response")

            output = r.text

            # Add the job results to our combined results array for all job items.
            single_job_result = {
		'adapter_type' : 'aigents',
		'service_type' : 'rss',
                'response_data': output
            }
            results.append(single_job_result)

        # Return the list of results that come from appending the results for the
        # individual job items in the job.
        return results

