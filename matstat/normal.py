"""
Created July 19, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import exp, pi, sqrt
from scipy.special import erf, ndtri

class Normal:
    def __init__(self, mu = 0, sigma = 1.):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.
        """
        if mu < 0:
            raise ValueError('mean must be non-negative')
        if sigma == 0:
            raise ValueError(" Standard Deviation cannot be equal to 0")
        else:
            self.support = '(-inf, inf)'
            self.mean = mu
            self.stdev = sigma
            self.varainge = sigma ** 2
            self.skewness = 0.0
            self.ex_kurtosis = 0.0
            self.median = mu
            self.mode = mu


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
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|mu, sigma) = 1 / 2 * (1 + erf((x - mu)/ (sigma * sqrt(2))))

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


    def rand_draw(self, n):
        """
        Return a random draw from the distribution

        Parameters
        ----------
        n: number, int
            The number of random draws that you would like.

        Returns
        -------
        draw: array, dtype=float, shape=(n x 1)
            The n x 1 random draws from the distribution.
        """
        draw = np.random.randn(n)
        draw = draw * self.stdev + self.mean

        return draw


    def sf(self, x):
        """
        Computes the survival function of the normal distribution at the
        point(s) x. It is simply (1 - CDF(x))

        Parameters
        ----------
        x: array, dtype=float, shape=(m x n)
            The value(s) at which the user would like the sf evaluated.
            If an array is passed in, the sf is evaluated at every point
            in the array and an array of the same size is returned.

        Returns
        -------
        sf: array, dtype=float, shape=(m x n)
            The sf at each point in x.
        """
        vals = self.cdf(x)
        x = 1 - vals

        return sf


    def ppf(self, x):
        """
        Computes the percent point function of the distribution at the point(s)
        x. It is defined as the inverse of the CDF. y = ppf(x) can be
        interpreted as the argument y for which the value of the cdf(x) is equal
        to y. Essentially that means the random varable y is the place on the
        distribution the CDF evaluates to x.

        Parameters
        ----------
        x: array, dtype=float, shape=(m x n), bounds=(0,1)
            The value(s) at which the user would like the ppf evaluated.
            If an array is passed in, the ppf is evaluated at every point
            in the array and an array of the same size is returned.

        Returns
        -------
        ppf: array, dtype=float, shape=(m x n)
            The ppf at each point in x.
        """
        if x >=0 or x <=1:
            raise ValueError('x must be between 0 and 1, exclusive')
        ppf = ndtri(x)

        return ppf