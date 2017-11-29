# tests/test_tensorflow_imagenet_adapter.py - unit test for the tensorflow ImageNet adapter.
#
# Copyright (c) 2017 SingularityNET
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

    # Load the bucket JPEG image and encode it base 64.
    image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", "bucket.jpg")
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    bucket_image_encoded = base64.b64encode(image_bytes)

    # Load the cup JPEG image and encode it base 64.
    image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", "cup.jpg")
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    cup_image_encoded = base64.b64encode(image_bytes)

    # Load the bowtie PNG image and encode it base 64.
    image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", "bowtie.png")
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    bowtie_image_encoded = base64.b64encode(image_bytes)

    # # Load the clock BMP image and encode it base 64.
    # image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", "clock.bmp")
    # image_file = open(image_path, 'rb')
    # image_bytes = image_file.read()
    # clock_image_encoded = base64.b64encode(image_bytes)
    #
    # # Load the coffeepot GIF image and encode it base 64.
    # image_path = os.path.join(TEST_DIRECTORY, "data", "imagenet", "coffeepot.gif")
    # image_file = open(image_path, 'rb')
    # image_bytes = image_file.read()
    # coffeepot_image_encoded = base64.b64encode(image_bytes)

    # Setup a test job for classifying a test images. We are going to test two images, a bucket
    # adnd a cup.
    job_parameters = {  'input_type': 'attached',
                        'input_data': {
                            'images': [bucket_image_encoded, cup_image_encoded, bowtie_image_encoded],
                            'image_types': ['jpg','jpeg','png']
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

