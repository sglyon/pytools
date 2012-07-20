"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt
import numpy as np
from scipy.special import beta, fdtr, fdtri

class F_dist:
    def __init__(self, d1=1, d2=2):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.
        """
        if d1 < 0 or d2 < 0 or type(d1) != int or type(d2) != int:
            raise ValueError('d1 and d2 must both be positive itegers.')

        self.d1 = d1
        self.d2 = d2
        self.support = '[0, inf)'
        self.mean = (d2 / (d2 - 2)) if d2 > 2 else None
        self.median = None
        self.mode = (d2 / d1) * ((d1 - 2) /  (d2 + 2)) if d2 > 2 else None
        self.variance = (2 * d2 ** 2 * (d1 + d2 - 2)) / \
                        (d1 * (d2 - 2) ** 2 * (d2 - 4)) if d2 > 4 else None
        self.skewness = (2 * d1 + d2 - 2) * sqrt(8 * (d2 - 4)) / \
                       ((d2 - 6) * sqrt(d1 * (d1 + d2 - 2))) if d2 > 6 else None
        self.ex_kurtosis = None


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|d1, d2) = sqrt((d1 * x) ** d1 * d2 ** d2 / ((d1 * x + d2)**(d1 + d2))) /\
             x * beta(d1 / 2, d2 / 2)

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
        d1 = self.d1
        d2 = self.d2
        pdf = np.sqrt((d1 * x) ** d1 * d2 ** d2 / ((d1 * x + d2)**(d1 + d2))) /\
             x * beta(d1 / 2, d2 / 2)
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
        cdf = fdtr(self.d1, self.d2, x)

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
        draw = np.random.f(self.d1, self.d2, n)

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
        ppf = fdtri(self.d1, self.d2, x)

        return ppf