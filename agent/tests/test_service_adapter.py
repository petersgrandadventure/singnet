#
# tests/test_service_adapter.py - unit test for the service adapters.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

import pytest

from sn_agent.ontology.base import TEST_SERVICE_NODE_5
from sn_agent.ontology.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter.base import ServiceAdapterABC
from tests.mock_app import MockApp

logger = logging.getLogger(__name__)


class MockServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, service: ServiceDescriptor):
        super().__init__(app, service, [])

    def perform(self, job: JobDescriptor):
        logger.debug('Performed job %s' % job)


def test_perform_services():
    with pytest.raises(Exception):
        mock_app = MockApp()
        mock_service = ServiceDescriptor(TEST_SERVICE_NODE_5)
        service_adapter = MockServiceAdapter(mock_app, mock_service)
        test_jobs = JobDescriptor.get_test_jobs()
        logger.debug('  Testing jobs')
        job = None
        try:
            exception_caught = False
            for job in test_jobs:
                logger.debug("testing job %s", job)
                service_adapter.perform(job)
        except RuntimeError:
            exception_caught = True
            logger.debug("Error performing %s %s", job, service_adapter)

        assert not exception_caught
