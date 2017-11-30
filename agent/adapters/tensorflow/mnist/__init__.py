#
# adapters/tensorflow/mnist/__init__.py - a service adapter for the tensorflow MNIST tutorial graph and dataset...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceManager, ServiceAdapterABC
from sn_agent.ontology import Service

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import tempfile
import os
from pathlib import Path

import logging

MNIST_CLASSIFIER_ID = 'deadbeef-aaaa-bbbb-cccc-111111111101'

logger = logging.getLogger(__name__)

FLAGS = None

AGENT_DIRECTORY = Path(__file__).parent

CHECK_ACCURACY = False


def conv2d(x, W):
    """conv2d returns a 2d convolution layer with full stride."""
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    """max_pool_2x2 downsamples a feature map by 2X."""
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def build_classifier_graph(input_images):
    """build_classifier_graph builds the graph for a deep net for classifying digits.

    Args:
        x: an input tensor with the dimensions (N_examples, 784), where 784 is the
        number of pixels in a standard MNIST image.

    Returns:
        A tuple (classifier_graph, keep_prob). classifier_graph is the final tensor of
        shape (N_examples, 10), with values equal to the logits of classifying the
        digit into one of 10 classes (the digits 0-9). keep_prob is a scalar placeholder
        for the probability of dropout.
    """

    # Reshape to use within a convolutional neural net.
    # Last dimension is for "features" - there is only one here, since images are
    # grayscale -- it would be 3 for an RGB image, 4 for RGBA, etc.
    with tf.name_scope('reshape'):
        reshaped_images = tf.reshape(input_images, [-1, 28, 28, 1])

    # First convolutional layer - maps one grayscale image to 32 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(reshaped_images, W_conv1) + b_conv1)

    # Pooling layer - downsamples by 2X.
    with tf.name_scope('pool1'):
        h_pool1 = max_pool_2x2(h_conv1)

    # Second convolutional layer -- maps 32 feature maps to 64.
    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # Second pooling layer.
    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)

    # Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
    # is down to 7x7x64 feature maps -- maps this to 1024 features.
    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([7 * 7 * 64, 1024])
        b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout - controls the complexity of the model, prevents co-adaptation of
    # features.
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Map the 1024 features to 10 classes, one for each digit
    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])

    classifier_graph = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    return classifier_graph, keep_prob


class TensorflowMNIST(ServiceAdapterABC):
    type_name = "TensorflowMNIST"

    def __init__(self, app, service: Service, required_services: List[Service] = None):
        super().__init__(app, service, required_services)
        if not service.node_id == MNIST_CLASSIFIER_ID:
            raise RuntimeError("TensorflowMNIST cannot perform service %s", service.node_id)

    def example_job(self):
        # A 28 x 28 image of a 7 which has been flattened into a single
        # float 784-element vector format as required by the tensorflow mnist adapter.
        return [
            {
                "input_type": "attached",
                "input_data": {
                    "images": [

                        [
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.32941177, 0.72549021, 0.62352943, 0.59215689, 0.23529413, 0.14117648,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0.8705883, 0.99607849, 0.99607849, 0.99607849, 0.99607849,
                            0.9450981, 0.77647066, 0.77647066, 0.77647066, 0.77647066, 0.77647066,
                            0.77647066, 0.77647066, 0.77647066, 0.66666669, 0.20392159, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0.26274511, 0.44705886, 0.28235295,
                            0.44705886, 0.63921571, 0.89019614, 0.99607849, 0.88235301, 0.99607849,
                            0.99607849, 0.99607849, 0.98039222, 0.89803928, 0.99607849, 0.99607849,
                            0.54901963, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0.06666667, 0.25882354,
                            0.05490196, 0.26274511, 0.26274511, 0.26274511, 0.23137257, 0.08235294,
                            0.92549026, 0.99607849, 0.41568631, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.32549021, 0.99215692, 0.81960791, 0.07058824, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.08627451, 0.91372555, 1., 0.32549021, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.50588238, 0.99607849, 0.9333334, 0.17254902, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.23137257, 0.97647065, 0.99607849, 0.24313727, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.52156866, 0.99607849, 0.73333335, 0.01960784, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.03529412, 0.80392164, 0.97254908, 0.227451, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.49411768, 0.99607849, 0.71372551, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.29411766, 0.98431379, 0.94117653, 0.22352943, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.07450981, 0.86666673, 0.99607849, 0.65098041, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.01176471, 0.7960785, 0.99607849, 0.8588236, 0.13725491, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.14901961, 0.99607849, 0.99607849, 0.3019608, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.12156864, 0.87843144, 0.99607849, 0.45098042, 0.00392157, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.52156866, 0.99607849, 0.99607849, 0.20392159, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0.2392157,
                            0.94901967, 0.99607849, 0.99607849, 0.20392159, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0.47450984, 0.99607849, 0.99607849, 0.8588236, 0.15686275, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0.47450984, 0.99607849, 0.81176478, 0.07058824, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0
                        ]

                    ]
                },
                "output_type": "attached"
            }
        ]

    def post_load_initialize(self, service_manager: ServiceManager):

        # Train the model or load a pretrained model from the cache.

        # There are member variables for the placeholders:
        #     self.input_images - images to be classified
        #     self.keep_prob - controls the dropout during training
        #
        # As well as member variables we need to have during perform:
        #     self.classifier_graph - the tensorflow graph for the image classifier
        #     self.model_path - the location of the cached model

        # Import data
        data_directory = os.path.join(AGENT_DIRECTORY, "input_data")
        mnist_data = input_data.read_data_sets(data_directory, one_hot=True)

        # Create the model - first initialize to default
        tf.reset_default_graph()

        # Define a placeholder for the images
        self.input_images = tf.placeholder(tf.float32, [None, 784])

        # Define loss and optimizer
        input_labels = tf.placeholder(tf.float32, [None, 10])

        # Build the graph for the deep neural network classifier
        self.classifier_graph, self.keep_prob = build_classifier_graph(self.input_images)

        with tf.name_scope('loss'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=input_labels, logits=self.classifier_graph)
        cross_entropy = tf.reduce_mean(cross_entropy)

        with tf.name_scope('adam_optimizer'):
            train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

        with tf.name_scope('accuracy'):
            correct_prediction = tf.equal(tf.argmax(self.classifier_graph, 1), tf.argmax(input_labels, 1))
            correct_prediction = tf.cast(correct_prediction, tf.float32)
        accuracy = tf.reduce_mean(correct_prediction)

        # Initialize the variables (i.e. assign their default value)
        initializer = tf.global_variables_initializer()

        # 'Saver' op to save and restore all the variables

        self.model_path = os.path.join(AGENT_DIRECTORY, "model_data", "model.ckpt")
        saver = tf.train.Saver()

        # Create our long-running Tensorflow session
        self.session = tf.Session()

        logger.debug("Checking for pre-trained model in {0}".format(self.model_path))
        if os.path.exists(self.model_path + ".index"):
            logger.debug("Restoring from pre-trained model")

            # Initialize variables
            self.session.run(initializer)

            # Restore model weights from previously saved model
            saver.restore(self.session, self.model_path)

            if CHECK_ACCURACY:
                accuracy = accuracy.eval(feed_dict={
                    self.input_images: mnist_data.test.images,
                    input_labels: mnist_data.test.labels,
                    self.keep_prob: 1.0})
                logger.debug("test accuracy {0}".format(accuracy))

        else:
            logger.debug("No checkpoint - training model from scratch")
            self.session.run(initializer)

            # Train the model
            for i in range(20000):
                batch = mnist_data.train.next_batch(50)
                if i % 100 == 0:
                    train_accuracy = accuracy.eval(feed_dict={
                        self.input_images: batch[0], input_labels: batch[1], self.keep_prob: 1.0})
                    logger.debug('step {0}, training accuracy {1}'.format(i, train_accuracy))
                train_step.run(feed_dict={
                    self.input_images: batch[0],
                    input_labels: batch[1],
                    self.keep_prob: 0.5})

            # Save model weights to disk
            save_path = saver.save(self.session, self.model_path)
            logger.debug("Model saved in file: {0}".format(save_path))

            if CHECK_ACCURACY:
                accuracy = accuracy.eval(feed_dict={
                    self.input_images: mnist_data.test.images,
                    input_labels: mnist_data.test.labels,
                    self.keep_prob: 1.0})
                logger.debug('Test accuracy {0}'.format(accuracy))

    def perform(self, job: JobDescriptor):

        # Process the items in the job. A single job may include a request to classify
        # many different images. Each item, in turn, may be an array of images.
        results = []
        for job_item in job:

            # Make sure the input type is one we can handle...
            input_type = job_item['input_type']
            if input_type != 'attached':
                logger.error("BAD input dict %s", str(job_item))
                raise RuntimeError("TensorflowMNIST - job item 'input_type' must be 'attached'.")

            # Get the images to classify, while making sure our job item dict is of the appropriate format.
            input_data = job_item['input_data']
            if input_data is None:
                raise RuntimeError("TensorflowMNIST - job item 'input_data' must be defined.")
            images_to_classify = input_data.get('images')
            if images_to_classify is None:
                raise RuntimeError("TensorflowMNIST - job item 'input_data' missing 'images'")

            # Get the predication and confidence for each image in this job item
            prediction = tf.argmax(self.classifier_graph, 1)
            confidence = tf.nn.softmax(self.classifier_graph)
            predictions = prediction.eval(session=self.session,
                                          feed_dict={self.input_images: images_to_classify, self.keep_prob: 1.0})
            confidences = confidence.eval(session=self.session,
                                          feed_dict={self.input_images: images_to_classify, self.keep_prob: 1.0})
            prediction_confidences = []
            for index in range(0, len(images_to_classify)):
                prediction_confidence = confidences[index][predictions[index]]
                prediction_confidences.append(float(prediction_confidence))

            logger.debug("Predictions: {0}".format(predictions))
            logger.debug("Confidences: {0}".format(prediction_confidences))

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'predictions': predictions.tolist(),
                'confidences': prediction_confidences,
            }
            results.append(single_job_result)

        return results
