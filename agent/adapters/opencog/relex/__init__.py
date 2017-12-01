#
# adapters/opencog/relex/__init__.py - an AI adapter that integrates the relex natural language parser...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import socket
import json
import time
from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)


class RelexAdapter(ServiceAdapterABC):
    type_name = "RelexAdapter"

    def __init__(self, app, service: Service, required_services: List[Service]) -> None:
        super().__init__(app, service, required_services)

        # Initialize member variables heres.
        self.response_template = None

    def example_job(self):
        return [
            {
                "input_type": "attached",
                "input_data": {"sentence": "The Singularity will come before we know it."},
                "output_type": "attached"
            },
            {

                "input_type": "attached",
                "input_data": {"sentence": "Will women robots rule the world?"},
                "output_type": "attached"
            }
        ]

    def post_load_initialize(self, service_manager: ServiceManager):
        super().post_load_initialize(service_manager)

    def get_attached_job_data(self, job_item: dict) -> dict:

        # Make sure the input type is one we can handle...
        input_type = job_item['input_type']
        if input_type != 'attached':
            logger.error("BAD input dict %s", str(job_item))
            raise RuntimeError("RelexAdapter - job item 'input_type' must be 'attached'.")

        # Pull the input data from the job item
        input_data = job_item['input_data']
        if input_data is None:
            raise RuntimeError("RelexAdapter - job item 'input_data' must be defined.")

        return input_data

    def relex_parse_sentence(self, sentence: str) -> dict:

        # Open a TCP socket
        relex_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time_out_seconds = 10.0
        relex_socket.settimeout(time_out_seconds)
        start_time = time.time();
        received_message = "NOT RECEIVED"

        try:
            # Connect to server and send data - note that "relex" below is the way to get to the
            # server running in another Docker container. See: docker_compose.yml
            relex_socket.connect(("relex", 9000))

            # Construct the message for the relex server. NOTE: It expects a "text: " at the
            # beginning and a "\n" at the end.
            relex_sentence = "text: " + sentence + "\n"

            # Send the sentence to the relex server.
            relex_socket.sendall(relex_sentence.encode('utf-8'))

            # Read the first parts
            received_chars = relex_socket.recv(1024)

            # Strip off the length from the message
            if b'\n' in received_chars:
                length_string, received_message = received_chars.split(b'\n', 1)
                bytes = int(length_string)
                bytes_left = bytes - len(received_message)

                # Read the rest if we don't already have the full JSON reply.
                while (len(received_chars) > 0 and
                        bytes_left > 0 and
                        time.time() - start_time < time_out_seconds):
                    received_chars = relex_socket.recv(bytes_left)
                    received_message = received_message + received_chars
                    bytes_left = bytes_left - len(received_chars)

            if (bytes_left > 0):
                raise RuntimeError("RelexAdapter - relex server timed out.")

            logger.debug("    relex server received message bytes: {0}".format(len(received_message)))

            # Decode this since the rest of the system expects unicode strings and not the
            # bytes returned from the socket.
            received_message = received_message.decode('utf-8')

            # Now parse the text since the JSON-RPC code expects a Python dict.
            parsed_message = json.loads(received_message)

        except socket.timeout:
            print("Socket timed out")
            raise RuntimeError("RelexAdapter - relex server timed out.")

        finally:
            relex_socket.close()

        return parsed_message


    def perform(self, job: JobDescriptor):
        logger.debug("Performing Relex parse job.")

        # Process the items in the job. The job may include many different sentences.
        results = []
        for job_item in job:

            # Get the input data for this job.
            job_data = self.get_attached_job_data(job_item)

            # Check to make sure we have the data required.
            sentence = job_data.get('sentence')
            if sentence is None:
                raise RuntimeError("RelexAdapter - job item 'input_data' missing 'sentence'")

            # Send the sentence to the relex server for parsing.
            parsed_sentence = self.relex_parse_sentence(sentence)

            # Append this job item results to our combined results array.
            single_job_result = {
                'relex_parse': parsed_sentence,
            }
            results.append(single_job_result)

        # Return the concatenated list of results of each of the individual job items.
        return results
