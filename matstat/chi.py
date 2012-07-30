"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
import numpy as np
from math import sqrt
from scipy.special import gamma, gammainc, gammaincinv
import matplotlib.pyplot as plt

class Chi:
    def __init__(self, k=1):
        """
        Initializes an object of chi distribution type. We instantiate the
        object as well as some common statistics about it. This will make sure
        k has acceptable values and raise a ValueError if it doesn't.

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
        [1]: www.http://mathworld.wolfram.com/ChiDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Chi_distribution
        [3]: scipy.stats.distributions
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
        draw = np.sqrt(np.random.chisquare(self.k, n))

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
        ppf = np.sqrt(2 * gammaincinv(k *.5, x))

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
        plt.title(r'$\chi$ (%.1f): PDF from %.2f to %.2f' %(self.k, low,  high))
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
        plt.title(r'$\chi$ (%.1f): PDF from %.2f to %.2f' %(self.k, low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([1.2, 1.5, 2.1, 5.4])
    x2 = np.array([.1, .3, .5, .9])
    k = 4
    chi = Chi(k)
    print 'support = ', chi.support
    print 'mean = ', chi.mean
    print 'median= ', chi.median
    print 'mode = ', chi.mode
    print 'variance = ', chi.variance
    print 'skewness = ', chi.skewness
    print 'Excess kurtosis = ', chi.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', chi.pdf(x)
    print 'cdf at x = ', chi.cdf(x)
    print 'ppf at x = ', chi.ppf(x2)
    print 'sf at x = ', chi.sf(x)
    print '6 random_draws ', chi.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 6)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 6)
    chi.plot_pdf(0, 6)
    chi.plot_cdf(0, 6)
