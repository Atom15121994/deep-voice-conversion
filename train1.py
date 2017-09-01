# -*- coding: utf-8 -*-
# /usr/bin/python2

from __future__ import print_function
from hyperparams import Hyperparams as hp
from tqdm import tqdm

from modules import *
from models import Model


def main():
    model = Model(mode="train1")

    # Loss
    loss_op = model.loss_net1()

    # Accuracy
    acc_op = model.acc_net1()

    # Training Scheme
    global_step = tf.Variable(0, name='global_step', trainable=False)
    optimizer = tf.train.AdamOptimizer(learning_rate=hp.lr)
    var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'net/net1')
    train_op = optimizer.minimize(loss_op, global_step=global_step, var_list=var_list)

    # Summary
    summ_op = summaries(loss_op, acc_op)

    session_conf = tf.ConfigProto(
        gpu_options=tf.GPUOptions(
            allow_growth=True,
        ),
    )
    # Training
    with tf.Session(config=session_conf) as sess:
        # Load trained model
        sess.run(tf.global_variables_initializer())
        model.load_variables(sess, 'train1')

        writer = tf.summary.FileWriter('logdir/train1', sess.graph)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        for epoch in range(1, hp.num_epochs + 1):
            for step in tqdm(range(model.num_batch), total=model.num_batch, ncols=70, leave=False, unit='b'):
                sess.run(train_op)

            # Write checkpoint files at every epoch
            summ, gs = sess.run([summ_op, global_step])
            writer.add_summary(summ, global_step=gs)

            if epoch % 5 == 0:
                tf.train.Saver().save(sess, 'logdir/train1/step_%d' % gs)

        coord.request_stop()
        coord.join(threads)


def summaries(loss, acc):
    for v in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'net/net1'):
        tf.summary.histogram(v.name, v)
    tf.summary.scalar('net1/train/loss', loss)
    tf.summary.scalar('net1/train/acc', acc)
    return tf.summary.merge_all()


if __name__ == '__main__':
    main()
    print("Done")