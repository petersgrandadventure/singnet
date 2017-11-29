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

MINIMUM_SCORE = 0.20


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
        # many different images. Each item, in turn, may include an array of images.
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
            image_types = input_data.get('image_types')
            if image_types is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' missing 'image_types'")

            # Clear the predictions for the new job item.
            predictions = []
            prediction_confidences = []

            # Classify all the images for this job item.
            for image, image_type in zip(images_to_classify, image_types):
                binary_image = base64.b64decode(image)
                if (image_type == 'jpeg' or image_type == 'jpg'):
                    decoder_key = 'DecodeJpeg/contents:0'
                elif  (image_type == 'png'):
                    decoder_key = 'DecodeJpeg/contents:0'
                elif (image_type == 'gif'):
                    decoder_key = 'DecodeGif/contents:0'
                    raise RuntimeError("TensorflowImageNet - cannot decode gif images")
                elif (image_type == 'bmp'):
                    decoder_key = 'DecodeBmp/contents:0'
                    raise RuntimeError("TensorflowImageNet - cannot decode bmp images")
                else:
                    decoder_key = 'DecodeJpeg/contents:0'
                    logger.warn("Missing image type {0}".format(image_type))

                raw_predictions = self.session.run(self.softmax_tensor, {decoder_key: binary_image})

                logger.debug("classifying '{0}' image".format(image_type))

                # Pull the predicted scorces out of the raw predictions.
                predicted_scores = raw_predictions[0]

                # Sort and strip off the top 5 predictions.
                top_predictions = predicted_scores.argsort()[-5:][::-1]
                image_predictions = []
                image_scores = []
                for predicted_node_id in top_predictions:

                    # Get a text description for the top predicted node.
                    description = self.node_lookup.id_to_string(predicted_node_id)

                    # Cast to a float so JSON can serialize it. Normal Tensorflow float32 are not serializable.
                    score = float(predicted_scores[predicted_node_id])

                    logger.debug("        prediction = '{0}', score = {1}".format(description, score))

                    # Add only those that exceed our minimum score to the predictions and scores lists.
                    if (score > MINIMUM_SCORE):
                        image_predictions.append(description)
                        image_scores.append(score)

                # Append the filtered predictions and scores for this image.
                predictions.append(image_predictions)
                prediction_confidences.append(image_scores)

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'predictions': predictions,
                'confidences': prediction_confidences,
            }
            results.append(single_job_result)

        return results
