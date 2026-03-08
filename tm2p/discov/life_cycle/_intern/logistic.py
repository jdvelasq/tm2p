import numpy as np


def logistic(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))
