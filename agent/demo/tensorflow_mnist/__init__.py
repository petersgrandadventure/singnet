#
# entity_extracter/__init__.py - demo agent service adapter...
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC
from sn_agent.ontology import Service

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import tempfile
import os
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


FLAGS = None

AGENT_DIRECTORY = Path(__file__).parent

CHECK_ACCURACY = False


def deepnn(input_images):
    """deepnn builds the graph for a deep net for classifying digits.

    Args:
        x: an input tensor with the dimensions (N_examples, 784), where 784 is the
        number of pixels in a standard MNIST image.

    Returns:
        A tuple (y, keep_prob). y is a tensor of shape (N_examples, 10), with values
        equal to the logits of classifying the digit into one of 10 classes (the
        digits 0-9). keep_prob is a scalar placeholder for the probability of
        dropout.
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

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
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

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    return y_conv, keep_prob


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


class TensorflowMNIST(ServiceAdapterABC):
    type_name = "TensorflowMNIST"

    def __init__(self, app, service: Service, required_services: List[Service] = None):
        super().__init__(app, service, required_services)

        # Import data
        data_directory = os.path.join(AGENT_DIRECTORY, "input_data")
        mnist = input_data.read_data_sets(data_directory, one_hot=True)
        self.mnist = mnist

        # Create the model
        tf.reset_default_graph()
        input_images = tf.placeholder(tf.float32, [None, 784])
        self.input_images = input_images

        # Define loss and optimizer
        input_labels = tf.placeholder(tf.float32, [None, 10])

        # Build the graph for the deep net
        y_conv, keep_prob = deepnn(input_images)
        self.y_conv = y_conv
        self.keep_prob = keep_prob

        with tf.name_scope('loss'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=input_labels, logits=y_conv)
        cross_entropy = tf.reduce_mean(cross_entropy)

        with tf.name_scope('adam_optimizer'):
            train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

        with tf.name_scope('accuracy'):
            correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(input_labels, 1))
            correct_prediction = tf.cast(correct_prediction, tf.float32)
        accuracy = tf.reduce_mean(correct_prediction)

        # Initialize the variables (i.e. assign their default value)
        iniitalizer = tf.global_variables_initializer()
        self.iniitalizer = iniitalizer

        # 'Saver' op to save and restore all the variables

        self.model_path = os.path.join(AGENT_DIRECTORY, "model_data", "model.ckpt")
        saver = tf.train.Saver()

        logger.debug("Checking for pre-trained model in {0}".format(self.model_path))
        if os.path.exists(self.model_path + ".index"):
            logger.debug("Restoring from pre-trained model")
            with tf.Session() as sess:
                # Initialize variables
                sess.run(iniitalizer)

                # Restore model weights from previously saved model
                saver.restore(sess, self.model_path)

                if CHECK_ACCURACY:
                    accuracy = accuracy.eval(feed_dict={
                        input_images: mnist.test.images,
                        input_labels: mnist.test.labels,
                        keep_prob: 1.0})
                    logger.debug("test accuracy {0}".format(accuracy))

        else:
            logger.debug("No checkpoint - training model from scratch")
            with tf.Session() as sess:
                sess.run(iniitalizer)
                for i in range(1000):
                    batch = mnist.train.next_batch(50)
                    if i % 100 == 0:
                        train_accuracy = accuracy.eval(feed_dict={
                            input_images: batch[0], input_labels: batch[1], keep_prob: 1.0})
                        logger.debug('step {0}, training accuracy {1}'.format(i, train_accuracy))
                    train_step.run(feed_dict={
                        input_images: batch[0],
                        input_labels: batch[1],
                        keep_prob: 0.5})

                # Save model weights to disk
                save_path = saver.save(sess, self.model_path)
                logger.debug("Model saved in file: {0}".format(save_path))

                if CHECK_ACCURACY:
                    accuracy = accuracy.eval(feed_dict={
                        input_images: mnist.test.images,
                        input_labels: mnist.test.labels,
                        keep_prob: 1.0})
                    logger.debug('Test accuracy {0}'.format(accuracy))

    def perform(self, job: JobDescriptor):
        with tf.Session() as sess:
            # Initialize variables
            sess.run(self.iniitalizer)

            # Restore model weights from previously saved model
            saver = tf.train.Saver()
            saver.restore(sess, self.model_path)

            for job_item in job:

                input_type = job_item['input_type']
                if not input_type is 'attached':
                    raise RuntimeError("TensorflowMNIST - job item 'input_type' must be 'attached'.")

                input_data = job_item['input_data']
                if input_data is None:
                    raise RuntimeError("TensorflowMNIST - job item 'input_data' must be defined.")
                prediction_images = input_data.get('images')
                if prediction_images is None:
                    raise RuntimeError("TensorflowMNIST - job item 'input_data' missing 'images'")

                # Get the predication and confidence for each element in the test slice
                prediction = tf.argmax(self.y_conv, 1)
                confidence = tf.nn.softmax(self.y_conv)
                predictions = prediction.eval(feed_dict={self.input_images: prediction_images, self.keep_prob: 1.0})
                confidences = confidence.eval(feed_dict={self.input_images: prediction_images, self.keep_prob: 1.0})
                prediction_confidences = []
                for index in range(0, len(prediction_images)):
                    prediction_confidence = confidences[index][predictions[index]]
                    prediction_confidences.append(prediction_confidence)

                logger.debug("Predictions: {0}".format(predictions))
                logger.debug("Confidences: {0}".format(prediction_confidences))

                results = {
                    'predictions': predictions,
                    'confidences': prediction_confidences,
                }
                return results
