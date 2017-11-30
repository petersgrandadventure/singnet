#
# document_summarizer/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#
import asyncio
import logging
import os
from typing import List

from examples.multi_agent_adapter.document_summarizer.settings import DocumentSummarizerSettings
from sn_agent import ontology
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)

DOCUMENT_SUMMARIZER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000001'
WORD_SENSE_DISAMBIGUATER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000002'
FACE_RECOGNIZER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000003'
TEXT_SUMMARIZER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000004'
VIDEO_SUMMARIZER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000005'
ENTITY_EXTRACTER_ID = 'deadbeef-aaaa-bbbb-cccc-000000000006'


class DocumentSummarizer(ServiceAdapterABC):
    type_name = "DocumentSummarizer"

    def __init__(self, app, service: Service, required_services: List[Service]) -> None:
        super().__init__(app, service, required_services)

        self.settings = DocumentSummarizerSettings()

        self.word_sense_disambiguater = None
        self.face_recognizer = None
        self.text_summarizer = None
        self.video_summarizer = None
        self.entity_extractor = None

    def example_job(self):
        return [
            {
                "input_type": "file",
                "input_url": "http://test.com/inputs/test_input.txt",
                "output_type": "file_url_put",
                "output_url": "test_output.txt"
            }
        ]

    def post_load_initialize(self, service_manager: ServiceManager):
        super().post_load_initialize(service_manager)

        self.word_sense_disambiguater = service_manager.get_service_adapter_for_id(WORD_SENSE_DISAMBIGUATER_ID)
        self.face_recognizer = service_manager.get_service_adapter_for_id(FACE_RECOGNIZER_ID)
        self.text_summarizer = service_manager.get_service_adapter_for_id(TEXT_SUMMARIZER_ID)
        self.video_summarizer = service_manager.get_service_adapter_for_id(VIDEO_SUMMARIZER_ID)
        self.entity_extractor = service_manager.get_service_adapter_for_id(ENTITY_EXTRACTER_ID)

    def transform_output_url(self, tag: str, item_count: int, output_url: str):
        last_part = output_url.split("/")[-1]
        if last_part == "":
            sub_adapter_output = tag + ".out"
        else:
            sub_adapter_output = tag + "_" + last_part
        sub_adapter_url = os.path.join(self.settings.TEST_OUTPUT_DIRECTORY, sub_adapter_output)
        return sub_adapter_url

    def sub_adapter_job(self, tag: str, sub_adapter: ServiceAdapterABC, job: JobDescriptor):
        new_service_descriptor = ServiceDescriptor(sub_adapter.service.node_id)
        new_job = JobDescriptor(new_service_descriptor)
        item_count = 0
        for job_item in job:

            # Just pass the inputs on directly to the subtasks.
            new_job_item = {
                'input_type': job_item['input_type'],
                'input_url': job_item['input_url']
            }

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
        logger.debug("      summarizing document")

        # Make sure we have a directory.
        directory = self.settings.TEST_OUTPUT_DIRECTORY
        if not os.path.exists(directory):
            os.mkdir(directory)

        # Create new job descriptors for the sub-services...
        word_job = self.sub_adapter_job('word', self.word_sense_disambiguater, job)
        face_job = self.sub_adapter_job('face', self.face_recognizer, job)
        text_job = self.sub_adapter_job('text', self.text_summarizer, job)
        video_job = self.sub_adapter_job('video', self.video_summarizer, job)
        entity_job = self.sub_adapter_job('entity', self.entity_extractor, job)

        self.word_sense_disambiguater.perform(word_job)
        self.face_recognizer.perform(face_job)
        self.text_summarizer.perform(text_job)
        self.video_summarizer.perform(video_job)
        self.entity_extractor.perform(entity_job)

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

    def perform_async(self, job: JobDescriptor):
        logger.debug("      summarizing document")

        # Make sure we have a directory.
        directory = self.settings.TEST_OUTPUT_DIRECTORY
        if not os.path.exists(directory):
            os.mkdir(directory)

        # Create new job descriptors for the sub-services...
        word_job = self.sub_adapter_job('word', self.word_sense_disambiguater, job)
        face_job = self.sub_adapter_job('face', self.face_recognizer, job)
        text_job = self.sub_adapter_job('text', self.text_summarizer, job)
        video_job = self.sub_adapter_job('video', self.video_summarizer, job)
        entity_job = self.sub_adapter_job('entity', self.entity_extractor, job)

        async def disambiguate_words():
            self.word_sense_disambiguater.perform(word_job)

        async def recognize_faces():
            self.face_recognizer.perform(face_job)

        async def summarize_text():
            self.text_summarizer.perform(text_job)

        async def summarize_video():
            self.video_summarizer.perform(video_job)

        async def extract_entities():
            self.entity_extractor.perform(entity_job)

        # Gather all the subservice tasks to process them asynchronously.
        loop = self.app.loop
        sub_services = [
            asyncio.ensure_future(disambiguate_words(), loop=loop),
            asyncio.ensure_future(recognize_faces(), loop=loop),
            asyncio.ensure_future(summarize_text(), loop=loop),
            asyncio.ensure_future(summarize_video(), loop=loop),
            asyncio.ensure_future(extract_entities(), loop=loop)]

        # Wait until the sub-service tasks all complete.
        results = asyncio.gather(*sub_services)

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
