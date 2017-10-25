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

from demo.tensorflow_mnist import TensorflowMNIST

mnist_seven_image =  [
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.32941177,  0.72549021,  0.62352943,  0.59215689,  0.23529413,  0.14117648,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.8705883,   0.99607849,  0.99607849,  0.99607849,  0.99607849,
  0.9450981,   0.77647066,  0.77647066,  0.77647066,  0.77647066,  0.77647066,
  0.77647066,  0.77647066,  0.77647066,  0.66666669,  0.20392159,  0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.26274511,  0.44705886,  0.28235295,
  0.44705886,  0.63921571,  0.89019614,  0.99607849,  0.88235301,  0.99607849,
  0.99607849,  0.99607849,  0.98039222,  0.89803928,  0.99607849,  0.99607849,
  0.54901963,  0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.06666667,  0.25882354,
  0.05490196,  0.26274511,  0.26274511,  0.26274511,  0.23137257,  0.08235294,
  0.92549026,  0.99607849,  0.41568631,  0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.32549021,  0.99215692,  0.81960791,  0.07058824,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.08627451,  0.91372555,  1.,          0.32549021,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.50588238,  0.99607849,  0.9333334,   0.17254902,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.23137257,  0.97647065,  0.99607849,  0.24313727,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.52156866,  0.99607849,  0.73333335,  0.01960784,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.03529412,  0.80392164,  0.97254908,  0.227451,    0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.49411768,  0.99607849,  0.71372551,  0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.29411766,  0.98431379,  0.94117653,  0.22352943,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.07450981,  0.86666673,  0.99607849,  0.65098041,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.01176471,  0.7960785,   0.99607849,  0.8588236,   0.13725491,  0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.14901961,  0.99607849,  0.99607849,  0.3019608,   0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.12156864,  0.87843144,  0.99607849,  0.45098042,  0.00392157,  0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.52156866,  0.99607849,  0.99607849,  0.20392159,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.2392157,
  0.94901967,  0.99607849,  0.99607849,  0.20392159,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,
  0.47450984,  0.99607849,  0.99607849,  0.8588236,   0.15686275,  0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.47450984,  0.99607849,  0.81176478,  0.07058824,  0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,          0.,          0.,          0.,
  0.,          0.,          0.,          0.,        ]

log = logging.getLogger(__name__)

TEST_DIRECTORY = Path(__file__).parent


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


# Utilities

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

    perform_one_service(app, service_manager, onto.DOCUMENT_SUMMARIZER_ID)
    perform_one_service(app, service_manager, onto.ENTITY_EXTRACTER_ID)
    perform_one_service(app, service_manager, onto.FACE_RECOGNIZER_ID)
    perform_one_service(app, service_manager, onto.TEXT_SUMMARIZER_ID)
    perform_one_service(app, service_manager, onto.VIDEO_SUMMARIZER_ID)
    perform_one_service(app, service_manager, onto.WORD_SENSE_DISAMBIGUATER_ID)

    start_stop_start_one_service(app, service_manager, onto.DOCUMENT_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, onto.ENTITY_EXTRACTER_ID)
    start_stop_start_one_service(app, service_manager, onto.FACE_RECOGNIZER_ID)
    start_stop_start_one_service(app, service_manager, onto.TEXT_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, onto.VIDEO_SUMMARIZER_ID)
    start_stop_start_one_service(app, service_manager, onto.WORD_SENSE_DISAMBIGUATER_ID)


def test_tensorflow_mnist_adapter(app):
    setup_logging()

    log.debug("Testing Tensorflow NNIST Adapter")

    job_parameters = {  'input_type': 'attached',
                        'input_data': {
                            'images': [mnist_seven_image],
                        },
                        'output_type': 'attached',
                 }

    service_id = onto.TENSORFLOW_MNIST_ID
    ontology = app['ontology']
    service = ontology.get_service(service_id)

    # Create a new job descriptor with four sets of parameters.
    job_list = [job_parameters]
    job = JobDescriptor(ServiceDescriptor(service_id), job_list)
    service_adapter = TensorflowMNIST(app, service)

    try:
        exception_caught = False
        results = service_adapter.perform(job)
    except RuntimeError as exception:
        exception_caught = True
        log.error("    Exception caught %s", exception)
        log.debug("    Error performing %s %s", job, service_adapter)
    assert not exception_caught

    assert results['predictions'] == [7]
    assert results['confidences'][0] > 0.9900


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
