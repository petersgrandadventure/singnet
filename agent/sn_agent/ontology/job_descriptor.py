#
# job_descriptor.py - implementation of abstract class defining API for service specs.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from sn_agent.ontology.base import TEST_SERVICE_NODE_1, TEST_SERVICE_NODE_2, TEST_SERVICE_NODE_3, TEST_SERVICE_NODE_4, TEST_SERVICE_NODE_5
from sn_agent.ontology.service_descriptor import ServiceDescriptor

class JobDescriptor(object):
    def __init__(self, service: ServiceDescriptor, job_parameters: dict):
        self.service = service
        self.job_parameters = job_parameters

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        description = self.service.name()
        return '<Job: service %s>' % description

    @classmethod
    def get_test_jobs(cls) -> []:
        test_jobs = []
        job_parameters = {'input_type': 'file',
                            'input_url': 'http://test.com/inputs/test_input.txt',
                            'output_type': 'file_url_put',
                            'output_url': 'http://test.com/outputs/test_output.txt'}
        test_jobs.append(JobDescriptor(ServiceDescriptor(TEST_SERVICE_NODE_1), job_parameters))
        test_jobs.append(JobDescriptor(ServiceDescriptor(TEST_SERVICE_NODE_2), job_parameters))
        test_jobs.append(JobDescriptor(ServiceDescriptor(TEST_SERVICE_NODE_3), job_parameters))
        test_jobs.append(JobDescriptor(ServiceDescriptor(TEST_SERVICE_NODE_4), job_parameters))
        test_jobs.append(JobDescriptor(ServiceDescriptor(TEST_SERVICE_NODE_5), job_parameters))
        return test_jobs
