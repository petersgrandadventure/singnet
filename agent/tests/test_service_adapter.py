# tests/test_service_adapter.py - unit test for the service adapters.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import os
from pathlib import Path

import pytest

from sn_agent import ontology as onto
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.job.job_descriptor import init_test_jobs
from sn_agent.log import setup_logging
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter import setup_service_manager, ServiceAdapterABC
from sn_agent.test.mocks import MockApp

import tests

log = logging.getLogger(__name__)

TEST_DIRECTORY = Path(__file__).parent

# Test fixtures and utilities

class MockServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, service: ServiceDescriptor):
        super().__init__(app, service, [])

    def perform(self, job: JobDescriptor):
        log.debug("      performed job %s", job)


@pytest.fixture
def app():
    app = MockApp()
    onto.setup_ontology(app)
    return app


# Tests

# Test performance of services - all of them
def test_perform_services(app):
    # The test jobs specify output URLs for files in an "output" directory inside the "tests" directory.

    print("current directory is ", os.getcwd())
    print("test directory is ", TEST_DIRECTORY)

    output_directory = os.path.join(TEST_DIRECTORY, "output")
    print("output directory is ", output_directory)
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    def remap_file_url(output_url: str):
        file_name = output_url.split("/")[-1]
        file_url = os.path.join(output_directory, file_name)
        return file_url

    def perform_one_service(app, service_manager, service_id):
        log.debug("  test_one_service")
        service_adapter = service_manager.get_service_adapter_for_id(service_id)
        test_jobs = JobDescriptor.get_test_jobs(service_id)

        # Remap the job item output URLs to the output directory.
        for job in test_jobs:
            for job_item in job:
                output_type = job_item['output_type']
                if output_type == 'file_url_put':
                    job_item['output_url'] = remap_file_url(job_item['output_url'])
                else:
                    raise RuntimeError("Bad output type %s for job %s" % (output_type, self))

        log.debug("    Testing jobs")
        job = None
        try:
            exception_caught = False
            for job in test_jobs:
                log.debug("      testing job %s", job)
                service_adapter.perform(job)
        except RuntimeError as exception:
            exception_caught = True
            log.error("    Exception caught %s", exception)
            log.debug("    Error performing %s %s", job, service_adapter)

        assert not exception_caught

    def start_stop_start_one_service(app, service_manager, service_id):
        log.debug("  start_stop_start_one_service")
        service_adapter = service_manager.get_service_adapter_for_id(service_id)
        try:
            exception_caught = False
            service_adapter.start()
            service_adapter.stop()
            service_adapter.start()
        except RuntimeError as exception:
            exception_caught = True
            log.error("    Exception caught %s", exception)
            log.debug("    Error starting or stopping %s", service_adapter)

        assert not exception_caught

    print()
    setup_logging()
    init_test_jobs()
    setup_service_manager(app)

    # Excercise the service manager methods.
    assert (not app['service_manager'] is None)
    service_manager = app['service_manager']

    perform_one_service(app, service_manager, tests.DOCUMENT_SUMMARIZER_ID)
    perform_one_service(app, service_manager, tests.ENTITY_EXTRACTER_ID)
    perform_one_service(app, service_manager, tests.FACE_RECOGNIZER_ID)
    perform_one_service(app, service_manager, tests.TEXT_SUMMARIZER_ID)
    perform_one_service(app, service_manager, tests.VIDEO_SUMMARIZER_ID)
    perform_one_service(app, service_manager, tests.WORD_SENSE_DISAMBIGUATER_ID)

    start_stop_start_one_service(app, service_manager, tests.DOCUMENT_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, tests.ENTITY_EXTRACTER_ID)
    start_stop_start_one_service(app, service_manager, tests.FACE_RECOGNIZER_ID)
    start_stop_start_one_service(app, service_manager, tests.TEXT_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, tests.VIDEO_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, tests.WORD_SENSE_DISAMBIGUATER_ID)

# Test performance of services - all of them
def test_bogus_yaml_config(app):
    print()
    setup_logging()

    # Test missing opencog ontology_node_id
    original_config_file = os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE']
    yaml_file = os.path.join(TEST_DIRECTORY, "service_adapter_test.yml")
    os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE'] = yaml_file
    exception_caught = False
    try:
        setup_service_manager(app)
    except RuntimeError as exception:
        exception_caught = True
        log.debug("    Expected Exception caught %s", exception)
    except:
        pass

    assert (exception_caught)

    # Test missing JSONRPC ontology_node_id
    yaml_file = os.path.join(TEST_DIRECTORY, "service_adapter_test_2.yml")
    os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE'] = yaml_file
    exception_caught = False
    try:
        setup_service_manager(app)
    except RuntimeError as exception:
        exception_caught = True
        log.debug("    Expected Exception caught %s", exception)
    except:
        pass

    assert (exception_caught)

    # Test missing Module ontology_node_id
    yaml_file = os.path.join(TEST_DIRECTORY, "service_adapter_test_3.yml")
    os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE'] = yaml_file
    exception_caught = False
    try:
        setup_service_manager(app)
    except RuntimeError as exception:
        exception_caught = True
        log.debug("    Expected Exception caught %s", exception)
    except:
        pass

    assert (exception_caught)

    # Test bogus service adapter type
    yaml_file = os.path.join(TEST_DIRECTORY, "service_adapter_test_4.yml")
    os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE'] = yaml_file
    exception_caught = False
    try:
        setup_service_manager(app)
    except RuntimeError as exception:
        exception_caught = True
        log.debug("    Expected Exception caught %s", exception)
    except:
        pass

    assert(exception_caught)


    # Reset to the original config file.
    os.environ['SN_SERVICE_ADAPTER_CONFIG_FILE'] = original_config_file

    setup_service_manager(app)
