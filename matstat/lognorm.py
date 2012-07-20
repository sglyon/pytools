"""
Created July 17, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import exp, sqrt, pi
from scipy.special import erf
from normal import Normal

class Lognorm:
    def __init__(self, mu = 0, sigma = 1.):
        """
        Initializes an object of distribution type. We instantiate the object
        as well as some common statistics about it. This will also check to
        make sure paramaters have acceptable values and raise a ValueError if
        they don't.
        """
        if mu < 0:
            raise ValueError('mean must be non-negative')
        else:
            self.support = '(0, inf)'
            self.mu = mu
            self.sigma = sigma
            self.mode = exp( mu - sigma ** 2)
            self.median = exp(mu)
            self.mean = exp((mu + sigma) / 2)
            self.variance = (exp(sigma**2) - 1) * exp(2 * mu + sigma ** 2)
            self.skewness = (exp(sigma ** 2) + 2) * sqrt(exp(sigma ** 2) - 1)
            self.ex_kurtosis = exp(4 * sigma ** 2) + 2 * exp(3 * sigma ** 2) + \
                               3 * exp(2 * sigma ** 2)  -6


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
        coef = 1 / (x * self.sigma * root_2_pi)
        pdf = np.exp(-((np.log(x) - self.mu) / (sqrt(2) * self.sigma)) ** 2)
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
        cdf = 1. / 2 * (1 + erf((np.log(x) - self.mu) /
                      (self.sigma * sqrt(2))))

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
        norm = Normal(self.mu, self.sigma)
        draw = np.exp(self.sigma * norm.rand_draw(n))

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
        norm = normal(self.mu, self.sigma)
        ppf = np.exp(self.sigma * norm.ppf(x))

        return ppf
