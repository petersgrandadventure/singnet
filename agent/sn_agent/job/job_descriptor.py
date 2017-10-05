#
# job_descriptor.py - implementation of abstract class defining API for service specs.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from sn_agent import ontology
from sn_agent.ontology.service_descriptor import ServiceDescriptor

test_jobs = {}

class JobDescriptor(object):
    def __init__(self, service: ServiceDescriptor, job_parameters: dict = None):
        self.service = service
        self.job_parameters = []
        if not job_parameters is None:
            self.job_parameters.append(job_parameters)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.service is None:
            description = ""
        else:
            description = self.service.name()
        return '<Job: service %s>' % (description)

    def __iter__(self):
        return self.job_parameters.__iter__()

    def __delitem__(self, key):
        self.job_parameters.__delitem__(key)
    def __getitem__(self, key):
        return self.job_parameters.__getitem__(key)
    def __setitem__(self, key, value):
        self.job_parameters.__setitem__(key, value)

    def __len__(self):
        return len(self.job_parameters)

    def append_job_item(self, job_item: dict):
        self.job_parameters.append(job_item)

    @classmethod
    def get_test_jobs(cls, service_id) -> []:
        return test_jobs[service_id]


def init_test_jobs():
    test_jobs[ontology.DOCUMENT_SUMMARIZER_ID] = []
    test_jobs[ontology.WORD_SENSE_DISAMBIGUATER_ID] = []
    test_jobs[ontology.FACE_RECOGNIZER_ID] = []
    test_jobs[ontology.TEXT_SUMMARIZER_ID] = []
    test_jobs[ontology.VIDEO_SUMMARIZER_ID] = []
    test_jobs[ontology.ENTITY_EXTRACTER_ID] = []

    job_parameters = {'input_type': 'file',
                        'input_url': 'http://test.com/inputs/test_input.txt',
                        'output_type': 'file_url_put',
                        'output_url': 'test_output.txt'}
    job_parameters_2 = {'input_type': 'file',
                        'input_url': 'http://test.com/inputs/test_input_2.txt',
                        'output_type': 'file_url_put',
                        'output_url': 'test_output_2.txt'}

    service_id = ontology.DOCUMENT_SUMMARIZER_ID
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters)
    test_jobs[service_id].append(job)
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters_2)
    test_jobs[service_id].append(job)

    service_id = ontology.WORD_SENSE_DISAMBIGUATER_ID
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters)
    test_jobs[service_id].append(job)
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters_2)
    test_jobs[service_id].append(job)

    service_id = ontology.FACE_RECOGNIZER_ID
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters)
    test_jobs[service_id].append(job)

    service_id = ontology.TEXT_SUMMARIZER_ID
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters)
    test_jobs[service_id].append(job)

    service_id = ontology.ENTITY_EXTRACTER_ID
    job = JobDescriptor(ServiceDescriptor(service_id), job_parameters)
    test_jobs[service_id].append(job)
