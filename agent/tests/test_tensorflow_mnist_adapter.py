# tests/test_tensorflow_mnist_adapter.py - unit test for the tensorflow MNIST adapter.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
from pathlib import Path

import pytest

from examples.tensorflow_mnist import TensorflowMNIST, MNIST_CLASSIFIER_ID
from sn_agent import ontology as onto
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.log import setup_logging
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter import setup_service_manager
from sn_agent.test.mocks import MockApp


# A 28 x 28 image of a 7 which has been flattened into a single float 784-element vector format
# as required by the tensorflow mnist adapter.
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


@pytest.fixture
def app():
    app = MockApp()
    onto.setup_ontology(app)
    return app


def test_tensorflow_mnist_adapter(app):
    setup_logging()
    log.debug("Testing Tensorflow NNIST Adapter")

    # Setup a test job for classifying a test mnist image. The test is a 28 x 28 image of a 7 which
    # has been flattened into a single float 784 element vector format as required by the tensorflow
    # example (see mnist_seven_image definition above).
    job_parameters = {  'input_type': 'attached',
                        'input_data': {
                            'images': [mnist_seven_image],
                        },
                        'output_type': 'attached',
                 }

    # Get the service for an MNIST classifier. A service identifies a unique service provided by
    # SingularityNET and is part of the ontology.
    ontology = app['ontology']
    mnist_service = ontology.get_service(MNIST_CLASSIFIER_ID)

    # Create the Tensorflow MNIST service adapter.
    mnist_service_adapter = TensorflowMNIST(app, mnist_service)

    # Create a service descriptor. These are post-contract negotiated descriptors that may include
    # other parameters like quality of service, input and output formats, etc.
    mnist_service_descriptor = ServiceDescriptor(MNIST_CLASSIFIER_ID)

    # Create a new job descriptor with a single set of parameters for the test image of a 7 in the
    # format defined above for the python variable: mnist_seven_image.
    job_list = [job_parameters]
    job = JobDescriptor(mnist_service_descriptor, job_list)

    # Setup the service manager. NOTE: This will add services that are (optionally) passed in
    # so you can manually create services in addition to those that are loaded from the config
    # file. After all the services are added, it will call post_load_initialize on all the
    # services.
    setup_service_manager(app, [mnist_service_adapter])

    # Test perform for the mnist service adapter.
    try:
        exception_caught = False
        results = mnist_service_adapter.perform(job)
    except RuntimeError as exception:
        exception_caught = True
        log.error("    Exception caught %s", exception)
        log.debug("    Error performing %s %s", job, service_adapter)
    assert not exception_caught

    # Check our results for format and content.
    assert len(results) == 1
    assert results[0]['predictions'] == [7]
    assert results[0]['confidences'][0] > 0.9900

    if results[0]['predictions'] == [7]:
        log.debug("Tensorflow NNIST Adapter - CORRECT evaluation of image as 7")
