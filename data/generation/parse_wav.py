#!/usr/bin/env python

import argparse

import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

class ParseWav(object):
    def __init__(self, filename, start_pos, num_points):
        self.filename = filename
        self.rate, self.signal = scipy.io.wavfile.read(filename)

        self.signal = self.signal.astype(np.float32)[start_pos:start_pos + num_points]
        self.normalize()

    def normalize(self):
        M = self.signal.max()
        m = self.signal.min()

        self.normalized_signal = -1.0 + 2.0 * (self.signal - m) / (M - m)

    def show_signal(self, normalized = True):
        plt.plot(self.normalized_signal if normalized else self.signal)
        plt.ylabel('Signal')
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Extract a normalized sequence of values from a WAV file.')
    parser.add_argument('--filename', type = str, help = 'WAV file to extract from', default = 'bad_taste.wav')
    parser.add_argument('--start-pos', type = int, help = 'Starting position of the signal', default = 0)
    parser.add_argument('--num-points', type = int, help = 'Number of points to extract', default = 320)
    args = parser.parse_args()

    parse_wav = ParseWav(args.filename, args.start_pos, args.num_points)

    # Plot the normalized signal
    parse_wav.show_signal()
