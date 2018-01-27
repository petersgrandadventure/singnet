#
# entity_extracter/__init__.py - demo agent service adapter...
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC

logger = logging.getLogger(__name__)


class EntityExtracter(ServiceAdapterABC):
    type_name = "EntityExtracter"

    def perform(self, job: JobDescriptor):
        item_count = 0
        for job_item in job:
            file_name = job[item_count]['output_url']
            with open(file_name, 'w') as file:
                file.write("entity:\n")
                file.write("    pig\n")
                file.write("    farmer\n")
                file.write("    tractor\n")
                file.write("    cornfield\n")
