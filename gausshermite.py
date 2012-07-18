"""
Created July 13, 2012

Author: Spencer Lyon
"""
import numpy as np
from numpy.polynomial.hermite import hermgauss

def gauss_hermite(N, mu, sigma):
    """
    This function computes the nodes and weights for gauss-hermite quadrature.
    It is assumed that the variable you are trying to model is distributed
    normally with mean = mu and variance = sigma.

    Parameters
    ----------
    N: number, int
        The number of nodes in the support and weight vectors.

    mu: numnber, float
        The mean of the random variable.

    sigma: number, float
         The standard deviation of the random variable.

    Returns
    -------
    eps: list (array), dtype = float, shape = (N x 1)
        The support vector for the random variable.

    weights: list (array), dtype = float, shape = (N x 1)
        The weights associated with the nodes in eps.

    Notes
    -----
    This function calls numpy.polynomial.hermite.hermgauss to create an initial
    version of the eps, and weights vectors. This function assumes the random
    variable follows the standard normal distribution.

    We take the results of that function and apply the following transformation
    to the nodes (assume eps_numpy are the return values from the numpy func):
        eps = mu + sigma * eps_numpy

    The weights are unchanged in the transformation
    """
    eps_numpy, weights = hermgauss(N)

    eps = mu + sigma * eps_numpy

    # Make sure probabilities sum to 1
    weights /= sum(weights)

    return [eps, weights]