"""
Created July 19, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import exp, pi, sqrt
from scipy.special import erf

class normal:
    def __init__(self, mu = 0, sigma = 1.):
        if mu < 0:
            raise ValueError('mean must be non-negative')
        if sigma == 0:
            raise ValueError(" Standard Deviation cannot be equal to 0")
        else:
            self.mean = mu
            self.stdev = sigma

    def pdf(self, x):
        """
        Computes the probability density function of the normal distribution
        at the point x. The pdf is defined as follows:
            f(x|mu, sigma) = 1/sqrt(2 * pi * sigma ** 2) * \
                             exp( - ((x - mu) / (sqrt(2) * sigma)) ** 2)

        Parameters
        ----------
            x: array, dtype=float, shape=(m x n)
                The value(s) at which the user would like the pdf evaluated.
                If an array is passed in, the pdf is evaluated at every point
                in the array and an array of the same size is returned.

        Returns
        -------
            pdf: array, dtype=float, shape=(m x n)
                The pdf at each point in x.
        """
        root_2_pi = sqrt(2 * pi)
        coef = 1. / (self.stdev * root_2_pi)
        pdf = np.exp( - ((x - self.mean) / (sqrt(2) * self.stdev)) ** 2)
        pdf *= coef

        return pdf

    def cdf(self, x):
        """
        Computes the cumulative distribution function of the normal
        distribution at the point(s) x. The pdf is defined as follows:
            f(x|mu, sigma) = 1/(x * sigma * sqrt(2 * pi)) * \
                             exp( - ((log(x) - mu) / (sqrt(2)* sigma)) ** 2)

        Parameters
        ----------
            x: array, dtype=float, shape=(m x n)
                The value(s) at which the user would like the cdf evaluated.
                If an array is passed in, the cdf is evaluated at every point
                in the array and an array of the same size is returned.

        Returns
        -------
            cdf: array, dtype=float, shape=(m x n)
                The cdf at each point in x.
        """
        cdf = 1 / 2. * (1 + erf((x - self.mean) / (self.stdev * sqrt(2))))

        return cdf
