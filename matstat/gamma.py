"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt
import numpy as np
from scipy.special import gamma as Fgamma
from scipy.special import gammainc, gammaincinv


class Gamma:
    """
    This distribution follos the form where k is the shape parameter and theta
    is the scale parameter rather then the alternative where alpha is the shape
    and beta is the rate parameter.

    If you want to pass in the rate you should say that theta= 1 / rate
    """
    def __init__(self, k=.5, theta=.5):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.

        Notes
        -----

        """
        if k < 0 or theta < 0:
            raise ValueError('k and theta must be positive')
        self.k = k
        self.theta = theta
        self.support = '[0, inf)'
        self.mean = k * theta
        self.median = None
        self.mode = (k - 1) * theta if k >= 1 else None
        self.variance = k * theta ** 2
        self.skewness = 2. / sqrt(k)
        self.ex_kurtosis = 6. / k


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|) =

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
        theta = self.theta
        pdf = 1 / (Fgamma(k) * theta ** k) * x ** (k - 1) * np.exp(-x / theta)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|) =

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
        cdf =  gammainc(self.k, x / self.theta) 

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
        draw = np.random.standard_gamma(self.k, n) * self.theta

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
        ppf = gammaincinv(self.k, x) * self.theta

        return ppf
