"""
Created July 20, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt
import numpy as np
from scipy.special import gamma as Fgamma
from scipy.special import gammainc as Fgammainc
from scipy.special import gammaincinv
import matplotlib.pyplot as plt

class Inverse_gamma:
    def __init__(self, alpha=1., beta=1.):
        """
        Initializes an object of inverse-gamma distribution type. We instantiate
        the object as well as some common statistics about it. This will make
        sure alpha and beta have acceptable values and raise a ValueError if
        either doesn't.

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
        This class is dependent on matplotlib, scipy, math, and numpy.

        References
        ----------
        [1]: www.http://en.wikipedia.org/wiki/Inverse-gamma_distribution
        [2]: scipy.stats.distributions
        """
        if alpha < 0 or beta < 0:
            raise ValueError('Both alpha and beta need to be positive')
        self.alpha = alpha
        self.beta = beta
        self.support = '(0, inf)'
        self.mean = beta / (alpha - 1) if alpha > 1 else None
        self.median = None
        self.mode = beta / (alpha + 1)
        self.variance = beta ** 2 / ((alpha - 1) ** 2 * (alpha - 2)) \
                        if alpha > 2 else None
        self.skewness = 4 * sqrt(alpha - 2) / (alpha - 2) if alpha > 3 else None
        self.ex_kurtosis = (30 * alpha - 66) / ((alpha - 3) * (alpha - 4)) \
                        if alpha > 4 else None


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|alpha, beta) = beta ** alpha * x ** (- alpha - 1) * \
                               np.exp(- beta / x) / Fgamma(alpha)

            where Fgamma is the gamma function

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
        beta = self.beta
        alpha = self.alpha
        pdf = beta ** alpha * x ** (- alpha - 1) * np.exp(- beta / x) / \
                Fgamma(alpha)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|alpha, beta) = Fgammainc(alpha, beta / x) / Fgamma(alpha)

        where Fgammainc and Fgamma are the upper incomplete gamma and gamma
        functions, respectively.

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
        cdf = 1 - Fgammainc(self.alpha, self.beta / x)

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
        U = np.random.sample(n)
        draw = self.ppf(U)

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

        ppf = 1. / gammaincinv(self.alpha, 1 - x)

        return ppf


    def plot_pdf(self, low, high):
        """
        Plots the pdf of the distribution from low to high.

        Parameters
        ----------
        low: number, float
            The lower bound you want to see on the x-axis in the plot.

        high: number, float
            The upper bound you want to see on the x-axis in the plot.

        Returns
        -------
        None

        Notes
        -----
        While this has no return values, the plot is generated and shown.
        """
        x = np.linspace(low, high, 300)
        plt.figure()
        plt.plot(x, self.pdf(x))
        plt.title(r'$\Gamma^-1(%.1f, %.1f)$: CDF from  %.2f to %.2f' %(self.alpha,
                                                                  self.beta,
                                                                  low,  high))
        plt.show()

        return


    def plot_cdf(self, low, high):
        """
        Plots the cdf of the distribution from low to high.

        Parameters
        ----------
        low: number, float
            The lower bound you want to see on the x-axis in the plot.

        high: number, float
            The upper bound you want to see on the x-axis in the plot.

        Returns
        -------
        None

        Notes
        -----
        While this has no return values, the plot is generated and shown.
        """
        x = np.linspace(low, high, 400)
        plt.figure()
        plt.plot(x, self.cdf(x))
        plt.title(r'$\Gamma^-1(%.1f, %.1f)$: CDF from  %.2f to %.2f' %(self.alpha,
                                                                  self.beta,
                                                                  low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([.1, .3, .4, .7])
    alpha = 3.
    beta = 1.
    gam = Inverse_gamma(alpha, beta)
    print 'support = ', gam.support
    print 'mean = ', gam.mean
    print 'median= ', gam.median
    print 'mode = ', gam.mode
    print 'variance = ', gam.variance
    print 'skewness = ', gam.skewness
    print 'Excess kurtosis = ', gam.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', gam.pdf(x)
    print 'cdf at x = ', gam.cdf(x)
    print '6 random_draws ', gam.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 3)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 3)
    gam.plot_pdf(0, 3)
    gam.plot_cdf(0, 3)
