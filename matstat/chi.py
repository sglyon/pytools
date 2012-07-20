"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
import numpy as np
from math import sqrt
from scipy.special import gamma, gammainc, gammaincinv

class Chi:
    def __init__(self, k=1):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.
        """
        if k < 0 or type(k) != int:
            raise ValueError('k must be a positive iteger')
        self.k = k
        self.support = '[0:inf)'
        self.mean = sqrt(2) * gamma((k +1) /2) / gamma(k / 2)
        self.median = None
        self.mode = sqrt(k) if k >=1 else None
        self.variance = k - self.mean ** 2
        self.skewness = (self.mean / self.variance ** 1.5) * \
                        (1 - 2 * self.variance)
        self.ex_kurtosis = (2 / self.variance) * (1 - self.mean *
                                                  sqrt(self.variance) *
                                                  self.skewness - self.variance)


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|k) =  2 ** (1 - k / 2) * x ** (k - 1) * np.exp((x ** 2) / 2) / \
                         gamma(k / 2)

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
        k = self.k
        pdf = 2 ** (1 - k / 2.) * x ** (k - 1.) * np.exp((-x ** 2.) / 2.) / \
                gamma(k / 2.)

        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|) = gammainc(K* .5, .5 x ** 2)
        Where gammainc is the regularized gamma function.

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
        cdf = gammainc(self.k* .5, .5 * x ** 2)

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
        draw = sqrt(np.random.chisquare(k, n))

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
        ppf = sqrt(2 * gammaincinv(k *.5, x))

        return ppf
