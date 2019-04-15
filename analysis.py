import numpy as np
from collections import Counter, OrderedDict
from OsloModel.logbin import logbin


def moving_average(data, temporal_window=50):
    """
    Produces an array of constant probability which is normalised over the whole data set.
    Mode ‘valid’ returns output of length max(M, N) - min(M, N) + 1. The convolution product is only given for points
    where the signals overlap completely. Values outside the signal boundary have no effect.
    :param data: The list of heights to average
    :param temporal_window: The size of the transient
    :return: The convolution of the data and the temporal_window
    """
    window = np.ones(temporal_window) / temporal_window
    return np.convolve(data, window, 'valid')

def calculate_probability(data):
    """
    The Counter object counts the number of occurences of a given height in the height_data set. Counter returns a
    dictionary object and sorted() orders the list in ascending order.
    :param data:
    :return: probabilities: The probability that a given height of the oslo_pile is likely to occur.
    """
    total_time = len(data)
    frequencies = sorted(Counter(data).items())
    probabilities = OrderedDict()
    for (key, value) in frequencies:
        probabilities[key] = value / total_time
    return probabilities


def log_bin(data, bin_scaling=1.3):
    """
    Allows for better statistical
    :param data: The size of avalanches in the recurrent configuration
    :param bin_scaling:
    :return:
    """
    centres, probabilities = logbin(data, scale=bin_scaling, zeros=False)
    return np.array(centres), np.array(probabilities)