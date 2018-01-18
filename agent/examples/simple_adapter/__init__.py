import logging
from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)


class SimpleAdapter(ServiceAdapterABC):
    type_name = "SimpleAdapter"

    def __init__(self, app, service: Service, required_services: List[Service]) -> None:
        super().__init__(app, service, required_services)

        # Initialize member variables here.
        self.response_template = None

    def example_job(self):
        return [
            {
                'input_type': 'attached',
                'input_data': {'simple_text': 'test'}
            }
        ]

    def post_load_initialize(self, service_manager: ServiceManager):
        super().post_load_initialize(service_manager)

        # Do any agent initialization here.
        self.response_template = "This AI takes the input and places it at the end: '{0}'."

    def get_attached_job_data(self, job_item: dict) -> dict:

        # Make sure the input type is one we can handle...
        input_type = job_item['input_type']
        if input_type != 'attached':
            logger.error("BAD input dict %s", str(job_item))
            raise RuntimeError("SimpleAdapter - job item 'input_type' must be 'attached'.")

        # Pull the input data from the job item
        input_data = job_item['input_data']
        if input_data is None:
            raise RuntimeError("SimpleAdapter - job item 'input_data' must be defined.")

        return input_data

    def perform(self, job: JobDescriptor):
        logger.debug("Performing SimpleAdapter job.")

        # Process the items in the job. The job may include many
        results = []
        for job_item in job:

            # Get the input data for this job.
            job_data = self.get_attached_job_data(job_item)

            # Check to make sure you have the data required.
            simple_text = job_data.get('simple_text')
            if simple_text is None:
                raise RuntimeError("SimpleAdapter - job item 'input_data' missing 'simple_text'")

            # Do the work... in this case we're just doing a simple text substitution into
            # our response template.
            simple_sentence = self.response_template.format(simple_text)

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'simple_sentence': simple_sentence,
            }
            results.append(single_job_result)

        # Return the list of results that come from appending the results for the
        # individual job items in the job.
        return results
