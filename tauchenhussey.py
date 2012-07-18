"""
Created July 11, 2012

Author: Spencer Lyon
    Borrowed from: Benjamin J. Tengelsen, Brigham Young University
                   Martin Floden, Stockholm School of Economics (original)
"""
from __future__ import division
import numpy as np
from numpy import zeros, sqrt, pi
import scipy.stats as st


def gausshermite(n):
    """
    This function finds the gauss hermite nodes and weights as outlined in
    "Numerical Recipies for C"

    Parameters
    ----------
    n: number, int
        The number of nodes to be found.

    Returns
    -------
    x: number, float


    w: number, float

    """
    MAXIT = 10
    EPS = 3e-14
    PIM4  = 0.7511255444649425

    x = zeros((n))
    w = zeros((n))

    m = (n+1)//2
    for i in range(1, m + 1):
        if i == 1:
            z = sqrt((2 * n + 1) - 1.85575 * (2 * n + 1) ** (-0.16667))
        elif i == 2:
            z = z - 1.14 * (n ** 0.426) / z
        elif i == 3:
            z = 1.86 * z - 0.86 * x[0]
        elif i == 4:
            z = 1.91 * z - 0.91 * x[1]
        else:
            z = 2 * z - x[i - 3];

        for iter in range(MAXIT):
            p1 = PIM4
            p2 = 0.0
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = z * sqrt(2. / j) * p2 - sqrt((j -1) / j) * p3
            pp = sqrt(2. * n) * p2
            z1 = z
            z = z1 - p1 / pp
            if abs(z - z1) <= EPS:
                break

        if iter > MAXIT:
            raise ValueError('Too many iterations')

        x[i - 1] = z
        x[n - i] = -z

        w[i - 1] = 2 / pp / pp
        w[n - i] = w[i - 1]

    x = x[::-1]

    return [x, w]


def gaussnorm(n, mu, s2):
    """
    This fuction finds the Gaussian nodes and weights for the normal
    distribution.

    Parameters
    ----------
    n: number, int
        The number of nodes

    mu: number, float
        The mean of the distribution

    s2: number, float
        The variance of the distribution.

    Returns
    -------
    x: number, float


    w: number, float

    """
    x0, w0 = gausshermite(n)
    x = x0 * sqrt(2 * s2) + mu
    w = w0 / sqrt(pi)
    return [x, w]


def tauchenhussey(N,mu,rho,sigma, baseSigma):
    """
    This function finds a markov chain/transition matrix to approximate the
    AR(1) process:
        z_{t+1} = (1 - rho ) * mu + z_{t} + eps(t + 1), eps ~ N(mu, sigma)

    Parameters
    ----------
    N: number, int
        This is the number of nodes desired in z.

    mu: number, float
        The mean of the normally distributed epsilon (eps) from above.

    rho: number, float
        The persistence parameter in the AR(1) process.

    sigma: number, float
        The standard deviation of epsilon (eps) from above.

    baseSigma: number, float
        The standard deviation used to calculate Guassian quadrature weights
        and nodes, i.e. to build the grid. I reccomend that you use:
            baseSigma = w * sigma + (1 - w) * sigmaZ
        where:
            sigmaZ = sigma / sqrt(1 - rho **2)
            w = 0.5 + rho / 4.0
        Tauchen and Hussey reccomend:
            baseSigma = sigma, or
            baseSigma = sigmaZ

    Returns
    -------
    Z: list (array), dtype = float
        The nodes for Z

    Zprob: 2D list (array), dtype = float
        The Markov transision matrix for the Z-nodes array.

    Notes
    -----
    This procedure is an implementation of Tauchen and  Hussey's algorithm,
    Econometric (1991, Vol. 59(2), pp. 371-396)
    """
    Zprob = zeros((N, N))

    [Z, w] = gaussnorm(N, mu, baseSigma**2)

    for i in range(N):
        for j in range(N):
            EZprime = (1 - rho) * mu + rho * Z[i]
            Zprob[i,j] = w[j] * st.norm.pdf(Z[j], EZprime, sigma) / \
                         st.norm.pdf(Z[j], mu, baseSigma)


    Zprob /= np.sum(Zprob, axis = 1)

    return [Z, Zprob]
