#
# tests/test_service_adapter.py - unit test for the service adapters.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import pytest

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent import ontology
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter.base import ServiceAdapterABC
from sn_agent.job.job_descriptor import init_test_jobs

log = logging.getLogger(__name__)


class MockApp(dict):
    def __init__(self):
        self['log'] = log
        pass

class MockServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, service: ServiceDescriptor):
        super().__init__(app, service, [])

    def perform(self, job: JobDescriptor):
        log.debug("      performed job %s", job)

@pytest.fixture
def app():
    app = MockApp()
    ontology.setup_ontology(app)
    return app

# Utilities

# Perform a single service
def perform_one_service(app, service_id):
    log.debug("  test_one_service")
    service = ServiceDescriptor(service_id)
    service_adapter = MockServiceAdapter(app, service)
    test_jobs = JobDescriptor.get_test_jobs(service_id)
    log.debug("    Testing jobs")
    job = None
    try:
        exception_caught = False
        for job in test_jobs:
            log.debug("      testing job %s", job)
            service_adapter.perform(job)
    except RuntimeError:
        exception_caught = True
        log.debug("    Error performing %s %s", job, service_adapter)

    assert not exception_caught

# Tests

# Test performance of services - all of them
def test_perform_services(app):
    init_test_jobs()
    perform_one_service(app, ontology.DOCUMENT_SUMMARIZER_ID)
    perform_one_service(app, ontology.ENTITY_EXTRACTER_ID)
    perform_one_service(app, ontology.FACE_RECOGNIZER_ID)
    perform_one_service(app, ontology.TEXT_SUMMARIZER_ID)
    perform_one_service(app, ontology.VIDEO_SUMMARIZER_ID)
    perform_one_service(app, ontology.WORD_SENSE_DISAMBIGUATER_ID)
