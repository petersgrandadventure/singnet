#
# adapters/tensorflow/imagenet/__init__.py - a service adapter for the tensorflow ImageNet pre-trained graph
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceManager, ServiceAdapterABC
from sn_agent.ontology import Service
from adapters.tensorflow.imagenet.node_lookup import NodeLookup

import tensorflow as tf
import os
import base64
from pathlib import Path

import logging

IMAGENET_CLASSIFIER_ID = 'deadbeef-aaaa-bbbb-cccc-111111111102'


logger = logging.getLogger(__name__)


FLAGS = None

AGENT_DIRECTORY = Path(__file__).parent

CHECK_ACCURACY = False




class TensorflowImageNet(ServiceAdapterABC):
    type_name = "TensorflowImageNet"

    def __init__(self, app, service: Service, required_services: List[Service] = None):
        super().__init__(app, service, required_services)
        if not service.node_id == IMAGENET_CLASSIFIER_ID:
            raise RuntimeError("TensorflowImageNet cannot perform service %s", service.node_id)

    def post_load_initialize(self, service_manager: ServiceManager):

        # Load the graph model.
        graph_path = os.path.join(AGENT_DIRECTORY, 'model_data', 'classify_image_graph_def.pb')
        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            self.graph_def = tf.GraphDef()
            self.graph_def.ParseFromString(f.read())
            tf.import_graph_def(self.graph_def, name='')

        # Create our long-running Tensorflow session
        self.session = tf.Session()

        # Save the softmax tensor which will run the model.
        self.softmax_tensor = self.session.graph.get_tensor_by_name('softmax:0')

        # Creates node ID --> English string lookup.
        self.node_lookup = NodeLookup()

    def perform(self, job: JobDescriptor):

        # Process the items in the job. A single job may include a request to classify
        # many different images. Each item, in turn, may be an array of images.
        results = []
        for job_item in job:

            # Make sure the input type is one we can handle...
            input_type = job_item['input_type']
            if input_type != 'attached':
                logger.error("BAD input dict %s", str(job_item))
                raise RuntimeError("TensorflowImageNet - job item 'input_type' must be 'attached'.")

            # Get the images to classify, while making sure our job item dict is of the appropriate format.
            input_data = job_item['input_data']
            if input_data is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' must be defined.")
            images_to_classify = input_data.get('images')
            if images_to_classify is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' missing 'images'")

            for image in images_to_classify:
                decoded_image = base64.b64decode(image)
                raw_predictions = self.session.run(self.softmax_tensor, {'DecodeJpeg/contents:0': decoded_image})

            # raw_predictions is a 1 element array with an X element array embedded

            logger.debug("Raw predictions[0] {0}, length = {1}".format(raw_predictions[0], len(raw_predictions[0])))

            # squeezed_predictions = numpy.squeeze(raw_predictions)
            squeezed_predictions = raw_predictions[0]

            logger.debug("Squeezed predictions {0}, length = {1}".format(squeezed_predictions, len(squeezed_predictions)))

            top_predictions = squeezed_predictions.argsort()[-5:][::-1]
            index = 0
            for predicted_node_id in top_predictions:
                index += 1
                human_string = self.node_lookup.id_to_string(predicted_node_id)
                score = squeezed_predictions[predicted_node_id]
                logger.debug("        prediction[{0}] = {1}, {2}".format(index, human_string, score))

            predictions = []
            prediction_confidences = []

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'predictions': predictions,
                'confidences': prediction_confidences,
            }
            results.append(single_job_result)

        return results
