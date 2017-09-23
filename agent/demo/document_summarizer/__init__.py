#
# document_summarizer/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter.base import ModuleServiceAdapterABC
from sn_agent.service_adapter.manager import ServiceManager
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent import ontology

log = logging.getLogger(__name__)


DOCUMENT_SUMMARIZER_ID          = 'deadbeef-aaaa-bbbb-cccc-000000000001'
WORD_SENSE_DISAMBIGUATER_ID     = 'deadbeef-aaaa-bbbb-cccc-000000000002'
FACE_RECOGNIZER_ID              = 'deadbeef-aaaa-bbbb-cccc-000000000003'
TEXT_SUMMARIZER_ID              = 'deadbeef-aaaa-bbbb-cccc-000000000004'
VIDEO_SUMMARIZER_ID             = 'deadbeef-aaaa-bbbb-cccc-000000000005'
ENTITY_EXTRACTER_ID             = 'deadbeef-aaaa-bbbb-cccc-000000000006'


class DocumentSummarizer(ModuleServiceAdapterABC):
    type_name = "DocumentSummarizer"

    def __init__(self, app, service_ontology_node, required_service_nodes, name: str):
        super().__init__(app, service_ontology_node, required_service_nodes, name)
        self.app = app

    def post_load_initialize(self, service_manager: ServiceManager):
        self.word_sense_disambiguater = service_manager.get_service_adapter_for_id(ontology.WORD_SENSE_DISAMBIGUATER_ID)
        self.face_recognizer = service_manager.get_service_adapter_for_id(ontology.FACE_RECOGNIZER_ID)
        self.text_summarizer = service_manager.get_service_adapter_for_id(ontology.TEXT_SUMMARIZER_ID)
        self.video_summarizer = service_manager.get_service_adapter_for_id(ontology.VIDEO_SUMMARIZER_ID)
        self.entity_extracter = service_manager.get_service_adapter_for_id(ontology.ENTITY_EXTRACTER_ID)

    def transform_output_url(self, sub_adapter: str, item_count: int, output_url: str):
        last_part = output_url.split("/")[-1]
        if last_part == "":
            output_url = sub_adapter + ".out"
        else:
            output_url = sub_adapter + last_part
        return output_url

    def perform(self, job: JobDescriptor):
        log.debug("        summarizing document")
        entity_service_descriptor = ServiceDescriptor(self.entity_extracter.service)
        entity_job = JobDescriptor(entity_service_descriptor)
        item_count = 0
        for job_item in job:
            entity_job_item = {}
            entity_job_item['input_type'] = job_item['input_type']
            output_type = job_item['output_type']
            entity_job_item['output_type'] = output_type

            entity_job_item['input_url'] = job_item['input_url']

            # Transform the output so we can get separate outputs for each sub-adapter.
            if output_type == 'file_url_put':
                output_url = job_item['output_url']
                sub_adapter_output_url = self.transform_output_url('entity', item_count, output_url)
                log.debug("        transformed job url for 'entity' to %s", sub_adapter_output_url)
            else:
                raise RuntimeError("Bad output type %s for job %s" % (output_type, self))
            entity_job_item['output_url'] = sub_adapter_output_url
            entity_job.append_job_item(entity_job_item)
            item_count += 1
