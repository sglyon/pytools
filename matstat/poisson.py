"""
Created July 20, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import floor, exp
import numpy as np
from scipy.special import pdtr, pdtrik
from scipy.misc import factorial
import matplotlib.pyplot as plt

class Poisson:
    def __init__(self, lamb=4):
        """
        Initializes an object of Poisson distribution type. We instantiate the
        object as well as some common statistics about it. This will also
        make sure lamb has acceptable values and raise a ValueError if it don't.

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
        This class is dependent on math, numpy, matplotlib, and scipy.

        References
        ----------
        [1]: www.http://mathworld.wolfram.com/PoissonDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Poisson_distribution
        [3]: scipy.stats.distributions
        """
        self.lamb = lamb
        self.support = 'k el {0, 2, 3, ...}'
        self.mean = lamb
        self.median = floor(lamb + 1 / 3 - 0.02 / lamb)
        self.mode = floor(lamb)
        self.variance = lamb
        self.skewness = lamb ** (-1 / 2)
        self.ex_kurtosis = 1. / lamb


    def pmf(self, x):
        """
        Computes the probability mass function of the distribution
        at the point x. The pdf is defined as follows:
            f(x| lamb, k) = lamb ** k / k! * exp( - lamb)

        Parameters
        ----------
            x: array, dtype=float, shape=(m x n)
                The value(s) at which the user would like the pmf evaluated.
                If an array is passed in, the pmf is evaluated at every point
                in the array and an array of the same size is returned.

        Returns
        -------
            pmf: array, dtype=float, shape=(m x n)
                The pmf at each point in x.
        """

        pmf = self.lamb ** x / factorial(x) * exp(- self.lamb)
        return pmf


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
        floored = np.floor(x)
        cdf = pdtr(floored, self.lamb)

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
        draw = np.random.poisson(self.lamb, n)

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
        vals = np.ceil(pdtrik(x, self.lamb))
        vals1 = vals - 1
        temp = ptdr(vals1, self.lamb)
        ppf = np.where((temp >= x), vals1, vals)

        return ppf


    def plot_pmf(self, low, high):
        """
        Plots the pdf of the distribution where k goes from low to high.

        Parameters
        ----------
        low: number, float
            The lower bound you want to see on the k in the plot.

        high: number, float
            The upper bound you want to see on the k in the plot.

        Returns
        -------
        None

        Notes
        -----
        While this has no return values, the plot is generated and shown.
        """
        low, high = int(min(low, high)), int(max(low, high))
        R = range(low, high)
        P = [self.pmf(k) for k in R]

        plt.figure()
        plt.plot(R, P, zorder=1, color='0.2', lw=1.5)
        plt.scatter(R, P, zorder=2, s=150, color='orange')
        plt.vlines(R, 0, P, alpha=0.4, colors='orange')


        plt.title(r'Poisson($\lambda$ = %.1f): PMF for k = %.2f to %.2f' \
                  %(self.lamb, low,  high))
        plt.axhline(color='k')
        plt.axvline(color='k')
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
        low, high = int(min(low, high)), int(max(low, high))
        R = range(low, high)
        P = [self.cdf(k) for k in R]

        plt.figure()
        plt.plot(R, P, zorder=1, color='0.2', lw=1.5)
        plt.fill_between(R, 0, P, color='orange', alpha=0.2)

        plt.title(r'Poisson($\lambda$ = %.1f): CDF for k = %.2f to %.2f' \
                  %(self.lamb, low,  high))
        plt.axhline(color='k')
        plt.axvline(color='k')
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([1, 3, 6, 7])
    lamb = 8
    poisson = Poisson(lamb)
    print 'support = ', poisson.support
    print 'mean = ', poisson.mean
    print 'median= ', poisson.median
    print 'mode = ', poisson.mode
    print 'variance = ', poisson.variance
    print 'skewness = ', poisson.skewness
    print 'Excess kurtosis = ', poisson.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', poisson.pmf(x)
    print 'cdf at x = ', poisson.cdf(x)
    print '6 random_draws ', poisson.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 20)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 20)
    poisson.plot_pmf(0, 20)
    poisson.plot_cdf(0, 20)
