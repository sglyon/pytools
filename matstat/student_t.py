"""
Created July 20, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt, pi
import numpy as np
from scipy.special import beta, gamma, stdtr, stdtrit

class Student_t:
    def __init__(self, nu=3):
        """
        Initializes an object of student-t distribution type. We instantiate the
        object as well as some common statistics about it. This will also make
        sure nu has acceptable values and raise a ValueError if it doesn't

        Methods
        -------
        pdf(x): pdf evaluated at each entry in x.
        cdf(x): cdf evaluated at each entry in x.
        rand_draw(n): n random draws from the distribution
        sf(x): survival function (1 - CDF) at x
        ppf(x): percent point function (inverse of cdf)
        plot_pdf(low, high): plots pdf with x going from low to high.
        plot_cdf(low, high): plots cdf with x going from low to high.

        Notes
        -----
        This class is dependent on matplotlib, scipy, and numpy.

        References
        ----------
        [1]: www.http://mathworld.wolfram.com/Studentst-Distribution.html
        [2]: www.http://en.wikipedia.org/wiki/Student_t_distribution
        [3]: scipy.stats.distributions
        """
        if type(nu) != int or nu < 0:
            raise ValueError('nu must be a positive integer')
        self.nu = nu
        self.support = '(-inf, inf)'
        self.mean =  0. if nu > 1 else None
        self.median = 0.
        self.mode = 0.
        self.variance = nu / (nu - 2) if nu > 2 else (None if nu<1 else np.inf)
        self.skewness =  0 if nu > 3 else None
        self.ex_kurtosis = 6 / (nu - 4) if nu > 4 else (None if n<2 else np.inf)


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|) = gamma((nu + 1)  / 2) / (sqrt(nu * pi) * gamma (nu / 2)) * \
                (1 + x ** 2 / nu) ** ( - ( nu + 1)  / 2)

        Where gamma is the gamma function.

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
        nu = self.nu
        pdf = gamma((nu + 1)  / 2) / (sqrt(nu * pi) * gamma (nu / 2)) * \
                (1 + x ** 2 / nu) ** ( - ( nu + 1)  / 2)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of they
        distribution at the point(s) x. The cdf is defined as follows:
            F(x| nu) = 1 - 1 / 2 *  I_x(t) *(nu / 2, 1 / 2)

        where x(t) = nu / (t ** 2 + u) and I_x is the regularized incomplete
        beta function.

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
        cdf = stdtr(self.nu, x)

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
        draw = np.random.standard_t(self.nu, n)

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
        ppf = stdtrit(self.nu, x)

        return ppf
