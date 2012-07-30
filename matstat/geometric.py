"""
Created July 23, 2012

Author: Spencer Lyon
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

class Geometric:
    def __init__(self, p=.6):
        """
        Initializes an object of Geometric distribution type. We instantiate the
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

        References: XXX
        ----------
        [1]: www.http://mathworld.wolfram.com/PoissonDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Poisson_distribution
        [3]: scipy.stats.distributions
        """
        if p > 1 or p <=0:
            raise ValueError('p must be an element of (0, 1])')
        self.p = p
        self.support = 'k el {0, 2, 3, ...}'
        self.mean = 1. / p
        self.median =  - 1/ (np.log2(1 - p))
        self.mode = 1.
        self.variance = (1 - p ) / (p **2)
        self.skewness = (2 - p ) / ((1 -p) **(1 / 2))
        self.ex_kurtosis = 6 + p **2 /(1 - p)


    def pmf(self, x):
        """
        Computes the probability mass function of the distribution
        at the point x. The pdf is defined as follows:
            f(x| p) = (1 - p) ** (x - 1) * p

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
        pmf = (1 -self.p) ** (x - 1) * self.p
        return pmf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|p) = 1 - (1 - p) ** x

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
        cdf = 1 - (1 - self.p) ** x

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
        draw = np.random.geometric(self.p, n)

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
        sf = 1 - vals

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
        if (x <=0).any() or (x >=1).any():
            raise ValueError('all values in x must be between 0 and 1, \
                             exclusive')
        vals = np.ceil(np.log(1. - x)  / np.log(1 - self.p))
        temp = 1. - (1. - self.p) ** ( vals - 1)
        ppf = np.where((temp >= x) & (vals > 0), vals - 1, vals)
        return ppf


    def plot_pmf(self, low, high):
        """
        Plots the pmf of the distribution where k goes from low to high.

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


        plt.title('Geometric(p = %.1f): PMF for k = %.2f to %.2f' %(self.p, low,
                                                                    high))
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

        plt.title('Geometric(p = %.1f): CDF for k = %.2f to %.2f' %(self.p, low,
                                                                    high))
        plt.axhline(color='k')
        plt.axvline(color='k')
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([1, 3, 6, 7])
    x2 = np.array([.1, .3, .5, .9])
    p = .3
    geo = Geometric(p)
    print 'support = ', geo.support
    print 'mean = ', geo.mean
    print 'median= ', geo.median
    print 'mode = ', geo.mode
    print 'variance = ', geo.variance
    print 'skewness = ', geo.skewness
    print 'Excess kurtosis = ', geo.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', geo.pmf(x)
    print 'cdf at x = ', geo.cdf(x)
    print 'ppf at x = ', geo.ppf(x2)
    print 'sf at x = ', geo.sf(x)
    print '6 random_draws ', geo.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 20)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 20)
    geo.plot_pmf(0, 20)
    geo.plot_cdf(0, 20)
