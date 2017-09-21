#
# tests/test_service_adapter.py - unit test for the service adapters.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import DOCUMENT_SUMMARIZER_ID, IMAGE_RECOGNIZER_ID, FACE_RECOGNIZER_ID, TEXT_SUMMARIZER_ID, \
    VIDEO_SUMMARIZER_ID
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter.base import ServiceAdapterABC
from sn_agent.ontology import Ontology

logger = logging.getLogger('test')



class MockServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, service: ServiceDescriptor):
        super().__init__(app, service, [])

    def perform(self, job: JobDescriptor):
        logger.debug('      performed job %s' % job)

def test_one_service(app, service_id):
    logger.debug('  test_one_service')
    service = ServiceDescriptor(service_id)
    service_adapter = MockServiceAdapter(app, service)
    test_jobs = JobDescriptor.get_test_jobs(service_id)
    logger.debug('    Testing jobs')
    job = None
    try:
        exception_caught = False
        for job in test_jobs:
            logger.debug("      testing job %s" % job)
            service_adapter.perform(job)
    except RuntimeError:
        exception_caught = True
        logger.debug("    Error performing %s %s" % job, service_adapter)

    assert not exception_caught


def test_perform_services(app):
    test_one_service(app, DOCUMENT_SUMMARIZER_ID)
    test_one_service(app, IMAGE_RECOGNIZER_ID)
    test_one_service(app, FACE_RECOGNIZER_ID)
    test_one_service(app, TEXT_SUMMARIZER_ID)
    test_one_service(app, VIDEO_SUMMARIZER_ID)
