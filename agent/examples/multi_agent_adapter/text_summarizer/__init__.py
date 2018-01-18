#
# text_summarizer/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC

logger = logging.getLogger(__name__)


class TextSummarizer(ServiceAdapterABC):
    type_name = "TextSummarizer"

    def perform(self, job: JobDescriptor):
        item_count = 0
        for job_item in job:
            file_name = job[item_count]['output_url']
            with open(file_name, 'w') as file:
                file.write("text:\n")
                file.write("    Farmer Jones and her husband, Henry, are standing in a field\n")
