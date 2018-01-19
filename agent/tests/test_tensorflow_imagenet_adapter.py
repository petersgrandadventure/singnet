#
# tests/test_tensorflow_imagenet_adapter.py - unit test for the tensorflow ImageNet adapter.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging
import os
from pathlib import Path
import base64

import pytest

from adapters.tensorflow.imagenet import TensorflowImageNet, IMAGENET_CLASSIFIER_ID
from sn_agent import ontology as onto
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.log import setup_logging
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter import setup_service_manager
from sn_agent.test.mocks import MockApp


log = logging.getLogger(__name__)

TEST_DIRECTORY = Path(__file__).parent


@pytest.fixture
def app():
    app = MockApp()
    onto.setup_ontology(app)
    return app


def test_tensorflow_imagenet_adapter(app):
    setup_logging()
    log.debug("Testing Tensorflow ImageNet Adapter")
    
    # images to be tested
    images = ["bucket.jpg", "cup.jpg", "bowtie.png"]
    encoded_images = []
    image_types = []

    for image in images:
        # Load each image and encode it base 64.
        image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", image)
        image_file = open(image_path, 'rb')
        image_bytes = image_file.read()
        encoded_images.append(base64.b64encode(image_bytes))
        image_types.append(image.split('.')[1])

    # Setup a test job for classifying the test images.
    job_parameters = {  'input_type': 'attached',
                        'input_data': {
                            'images': encoded_images,
                            'image_types': image_types
                        },
                        'output_type': 'attached',
                    }

    # Get the service for an ImageNet classifier. A service identifies a unique service provided by
    # SingularityNET and is part of the ontology.
    ontology = app['ontology']
    imagenet_service = ontology.get_service(IMAGENET_CLASSIFIER_ID)

    # Create the Tensorflow ImageNet service adapter.
    imagenet_service_adapter = TensorflowImageNet(app, imagenet_service)

    # Create a service descriptor. These are post-contract negotiated descriptors that may include
    # other parameters like quality of service, input and output formats, etc.
    imagenet_service_descriptor = ServiceDescriptor(IMAGENET_CLASSIFIER_ID)

    # Create a new job descriptor with a single set of parameters for the test image of a 7 in the
    # format defined above for the python variable: mnist_seven_image.
    job_list = [job_parameters]
    job = JobDescriptor(imagenet_service_descriptor, job_list)

    # Setup the service manager. NOTE: This will add services that are (optionally) passed in
    # so you can manually create services in addition to those that are loaded from the config
    # file. After all the services are added, it will call post_load_initialize on all the
    # services.
    setup_service_manager(app, [imagenet_service_adapter])

    # Test perform for the ImageNet service adapter.
    try:
        exception_caught = False
        results = imagenet_service_adapter.perform(job)
    except RuntimeError as exception:
        exception_caught = True
        log.error("    Exception caught %s", exception)
        log.debug("    Error performing %s %s", job, imagenet_service_adapter)
    assert not exception_caught

    print(results)

    # Check our results for format and content.
    assert len(results) == 1
    assert results[0]['predictions'] == [['bucket, pail'],['cup','coffee mug'],['bow tie, bow-tie, bowtie']]
    assert results[0]['confidences'][0][0] > 0.9600 and results[0]['confidences'][2][0] < 1.0
    assert results[0]['confidences'][1][0] > 0.4000 and results[0]['confidences'][1][1] < 0.4200
    assert results[0]['confidences'][1][1] > 0.4000 and results[0]['confidences'][1][1] < 0.4100
    assert results[0]['confidences'][2][0] > 0.9990 and results[0]['confidences'][2][0] < 1.0

