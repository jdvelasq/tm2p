import numpy as np


def logistic_derivative(t, K, r, t0):
    exp_term = np.exp(-r * (t - t0))
    return K * r * exp_term / (1 + exp_term) ** 2
