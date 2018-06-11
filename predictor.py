import tensorflow as tf
import pandas as pd
import numpy as np


def neural(img,l):
    x = np.array(img,dtype = np.float32)
    images = x.reshape(l, 784)

    images = np.multiply(images, 1.0 / 255.0)

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph("covnet/model57900.ckpt.meta")
        saver.restore(sess, tf.train.latest_checkpoint("covnet/"))
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        y = graph.get_tensor_by_name("h_fc6:0")
        pred = tf.argmax(y, 1)
        op = np.array((sess.run(pred, feed_dict={x: images})))
    return op
