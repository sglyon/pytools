"""
Created July 19, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import sqrt
from scipy.special import beta as Fbeta
from scipy.special import btdtr, btdtri

class Beta:
    def __init__(self, alpha=.1, beta=.1):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.
        """
        if alpha < 0 or beta < 0:
            raise ValueError('mean must be non-negative')
        else:
            self.support = '(0, 1)'
            self.alpha = alpha
            self.beta = beta
            self.mean = alpha / (alpha + beta)
            self.median = None
            self.mode = (alpha - 1) / (alpha + beta - 2) \
                        if (alpha > 1 and beta > 1) else None
            self.variance = alpha * beta / ((alpha + beta ) **2 +
                                            (alpha + beta +1))
            self.skewness = (2 * (beta - alpha ) * sqrt(alpha + beta + 1)) / \
                             ((alpha + beta + 2) * sqrt(alpha * beta))
            self.ex_kurtosis = None


    def pdf(self, x):
        """
        Computes the probability density function of the  beta distribution
        at the point x. The pdf is defined as follows (alpha -> a, beta -> b):
            f(x|a, b) =(x ** (a - 1) * (1 - x) **(b - 1)) / Fbeta(a, b)

        Where Fbeta is the beta function.

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
        alpha = self.alpha
        beta = self.beta
        pdf = (x ** (alpha - 1) * (1 - x) **(beta - 1)) / Fbeta(alpha, beta)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows (where
        alpha->a beta ->b, Fbetainc is incomplete beta function and Fbeta is the
        complete beta function):
            F(x|a, b) = Fbetainc(a, b, x) / Fbeta(a, b)

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
        alpha = self.alpha
        beta = self.beta
        cdf = btdtr(alpha, beta, x)

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
        draw = np.random.beta(self.alpha, self.beta, n)

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
        ppf = btdtri(self.alpha, self.beta, x)

        return ppf
