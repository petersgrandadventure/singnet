#
# document_summarizer/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#
from demo.document_summarizer.settings import DocumentSummarizerSettings
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter.base import ModuleServiceAdapterABC
from sn_agent.service_adapter.manager import ServiceManager
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent import ontology
import os
import asyncio

import logging

log = logging.getLogger(__name__)


class DocumentSummarizer(ModuleServiceAdapterABC):
    type_name = "DocumentSummarizer"

    def __init__(self, app, service_ontology_node, required_service_nodes, name: str):
        super().__init__(app, service_ontology_node, required_service_nodes, name)
        self.app = app
        self.settings = DocumentSummarizerSettings()

    def post_load_initialize(self, service_manager: ServiceManager):
        self.word_sense_disambiguater = service_manager.get_service_adapter_for_id(ontology.WORD_SENSE_DISAMBIGUATER_ID)
        self.face_recognizer = service_manager.get_service_adapter_for_id(ontology.FACE_RECOGNIZER_ID)
        self.text_summarizer = service_manager.get_service_adapter_for_id(ontology.TEXT_SUMMARIZER_ID)
        self.video_summarizer = service_manager.get_service_adapter_for_id(ontology.VIDEO_SUMMARIZER_ID)
        self.entity_extracter = service_manager.get_service_adapter_for_id(ontology.ENTITY_EXTRACTER_ID)

    def transform_output_url(self, tag: str, item_count: int, output_url: str):
        last_part = output_url.split("/")[-1]
        if last_part == "":
            sub_adapter_output = tag + ".out"
        else:
            sub_adapter_output = tag + "_" + last_part
        sub_adapter_url = os.path.join(self.settings.TEST_OUTPUT_DIRECTORY, sub_adapter_output)
        return sub_adapter_url

    def sub_adapter_job(self, tag: str, sub_adapter: ModuleServiceAdapterABC, job: JobDescriptor):
        new_service_descriptor = ServiceDescriptor(sub_adapter.service)
        new_job = JobDescriptor(new_service_descriptor)
        item_count = 0
        for job_item in job:

            # Just pass the inputs on directly to the subtasks.
            new_job_item = {}
            new_job_item['input_type'] = job_item['input_type']
            new_job_item['input_url'] = job_item['input_url']

            output_type = job_item['output_type']
            new_job_item['output_type'] = output_type

            # Transform the output URL so we can get separate output files for each sub-adapter
            # That way we can assemble the various parts at the end using these separate URLs.
            if output_type == 'file_url_put':
                output_url = job_item['output_url']
                sub_adapter_output_url = self.transform_output_url(tag, item_count, output_url)
            else:
                raise RuntimeError("Bad output type %s for job %s" % (output_type, self))
            new_job_item['output_url'] = sub_adapter_output_url
            new_job.append_job_item(new_job_item)

            item_count += 1
        return new_job

    def copy_adapter_output(self, output_file, input_file_name: str, tag: str):
        with open(input_file_name) as input_file:
            for line in input_file:
                output_file.write(line)
            output_file.write("\n")

    def perform(self, job: JobDescriptor):
        log.debug("      summarizing document")

        # Make sure we have a directory.
        directory = self.settings.TEST_OUTPUT_DIRECTORY
        if not os.path.exists(directory):
            os.mkdir(directory)

        # Create new job descriptors for the sub-services...
        word_job = self.sub_adapter_job('word', self.word_sense_disambiguater, job)
        face_job = self.sub_adapter_job('face', self.face_recognizer, job)
        text_job = self.sub_adapter_job('text', self.text_summarizer, job)
        video_job = self.sub_adapter_job('video', self.video_summarizer, job)
        entity_job = self.sub_adapter_job('entity', self.entity_extracter, job)

        async def disambiguate_words():
            self.word_sense_disambiguater.perform(word_job)

        async def recognize_faces():
            self.face_recognizer.perform(face_job)

        async def summarize_text():
            self.text_summarizer.perform(text_job)

        async def summarize_video():
            self.video_summarizer.perform(video_job)

        async def extract_entities():
            self.entity_extracter.perform(entity_job)

        # Gather all the subservice tasks to process them asynchronously.
        loop = self.app.loop
        sub_services = [
            asyncio.ensure_future(disambiguate_words(), loop=loop),
            asyncio.ensure_future(recognize_faces(), loop=loop),
            asyncio.ensure_future(summarize_text(), loop=loop),
            asyncio.ensure_future(summarize_video(), loop=loop),
            asyncio.ensure_future(extract_entities(), loop=loop)]

        # Wait until the sub-service tasks all complete.
        loop.run_until_complete(asyncio.gather(*sub_services))

        # Now copy the outputs of each of the sub-jobs...
        item_count = 0
        for job_item in job:
            output_file_name = self.transform_output_url('document', item_count, job_item['output_url'])

            with open(output_file_name, "w") as output_file:
                self.copy_adapter_output(output_file, word_job[item_count]['output_url'], 'word')
                self.copy_adapter_output(output_file, face_job[item_count]['output_url'], 'face')
                self.copy_adapter_output(output_file, text_job[item_count]['output_url'], 'text')
                self.copy_adapter_output(output_file, video_job[item_count]['output_url'], 'video')
                self.copy_adapter_output(output_file, entity_job[item_count]['output_url'], 'entity')

            item_count += 1
