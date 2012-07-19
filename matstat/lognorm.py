"""
Created July 17, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import sqrt, pi
from normal import normal
from scipy.special import erf

class lognorm:
    def __init__(self, mu = 0, sigma = 1.):
        if mu < 0:
            raise ValueError('mean must be non-negative')
        else:
            self.mean = mu
            self.stdev = sigma

    def pdf(self, x):
        """
        Computes the probability density function of the lognorm distribution
        at the point x. The pdf is defined as follows:
            f(x|mu, sigma) = 1/(x * sigma * sqrt(2 * pi)) * \
                             exp( - ((log(x) - mu) / (sqrt(2)* sigma)) ** 2)

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
        coef = 1 / (x * self.stdev * root_2_pi)
        pdf = np.exp(-((np.log(x) - self.mean) / (sqrt(2) * self.stdev)) ** 2)
        pdf *= coef

        return pdf

    def cdf(self, x):
        """
        Computes the cumulative distribution function of the log-normal
        distribution at the point x. The pdf is defined as follows:
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
        cdf = 1. / 2 * (1 + erf((np.log(x) - self.mean) /
                      (self.stdev * sqrt(2))))

        return cdf
