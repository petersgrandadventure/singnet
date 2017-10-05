#
# text_summarizer/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter.base import ModuleServiceAdapterABC

import logging

log = logging.getLogger(__name__)

class TextSummarizer(ModuleServiceAdapterABC):
    type_name = "TextSummarizer"

    def __init__(self, app, service_ontology_node, required_service_nodes, name: str):
        super().__init__(app, service_ontology_node, required_service_nodes, name)

    def perform(self, job: JobDescriptor):
        item_count = 0
        for job_item in job:
            file_name = job[item_count]['output_url']
            with open(file_name, 'w') as file:
                file.write("text:\n")
                file.write("    Farmer Jones and her husband, Henry, are standing in a field\n")
