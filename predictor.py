import tensorflow as tf
import pandas as pd
import numpy as np


def neural(x):
    images = x.reshape(1, 784)
    images = images.astype(np.float)

    images = np.multiply(images, 1.0 / 255.0)

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph("covnet/model57900.ckpt.meta")
        saver.restore(sess, tf.train.latest_checkpoint("covnet/"))
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        y = graph.get_tensor_by_name("h_fc6:0")
        pred = tf.argmax(y, 1)
        op = int(sess.run(pred, feed_dict={x: images}))

    val = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'A', 11: 'B', 12: 'C',
           13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N',
           24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y',
           35: 'Z', 36: 'a', 37: 'b', 38: 'd', 39: 'e', 40: 'f', 41: 'g', 42: 'h', 43: 'n', 44: 'q', 45: 'r', 46: 't'}
    return val[op]
