#!/usr/bin/env python

import argparse

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from data.generation.parse_wav import ParseWav
from models.clockwork_rnn import ClockworkRNN
from models.lstm import LSTM

if __name__ == '__main__':
    ### Dataset & training configuration ###
    config = {
        'input_dim': 0,
        'hidden_dim': 36,
        'output_dim': 1,
        'periods': [1, 2, 4, 8, 16, 32, 64, 128, 256],
        'num_steps': 320,

        'learning_rate': 1e-2,
        'learning_rate_step': 50,
        'learning_rate_decay': 0.9,
        'optimizer': 'rmsprop',
        'momentum': 0.95,
        'max_epochs': 1000
    }

    ### Create the model ###
    model_type = 'clockwork_rnn'

    if model_type == 'clockwork_rnn':
        model = ClockworkRNN(config)
        print('The Clockwork RNN has {} parameters'.format(model.num_parameters))
    elif model_type == 'lstm':
        model = LSTM(config)
        print('The LSTM has {} parameters'.format(model.num_parameters))

    # Change this for a different logging subfolder
    experiment_name = '{}_{}params'.format(model_type, model.num_parameters)

    ### Load data ###

    # Use fake data: generated from a sinusoid
    # targets = np.reshape(np.sin(np.arange(config['num_steps'])), (config['num_steps'], config['output_dim']))

    # Use a WAV file and normalize it
    parse_wav = ParseWav('data/generation/bad_taste.wav', 0, config['num_steps'])
    # Reshape signal for model
    targets = parse_wav.normalized_signal.reshape((-1, 1))
    # Plot signal
    # parse_wav.show_signal()

    ### Create a session ###
    with tf.Session() as sess:
        # Initialize variables
        tf.global_variables_initializer().run()

        # Create a writer
        log_writer = tf.summary.FileWriter('results/log/' + experiment_name, sess.graph, flush_secs = 2)

        data_dict = {
            model.inputs: np.zeros((config['num_steps'], config['input_dim'])),
            model.targets: targets
        }

        ### Train for several epochs ###
        for epoch in range(config['max_epochs']):
            results = sess.run([model.train_step, model.summaries],
                feed_dict = data_dict)

            log_writer.add_summary(results[1], global_step = tf.train.global_step(sess, model.global_step))

        # After training, do a final pass evaluate & plot the result
        error, outputs = sess.run([model.loss, model.outputs], feed_dict = data_dict)
        outputs = outputs.reshape(-1)
        ground_truth = targets.reshape(-1)

        # Final result
        print('')
        print('')
        print('After {} epochs, error is {}'.format(config['max_epochs'], error))

        plt.plot(ground_truth, '--')
        plt.plot(outputs)
        plt.legend(['Target signal', '{} output'.format(model_type)])
        plt.show()
