"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
import numpy as np
from math import sqrt
from scipy.special import gamma, chdtr, chdtri
import matplotlib.pyplot as plt

class Chi_square:
    def __init__(self, k=2):
        """
        Initializes an object of chi-squared distribution type. We instantiate
        the object as well as some common statistics about it. This will make
        sure k has acceptable values and raise a ValueError if it doesn't.

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
        [1]: www.http://mathworld.wolfram.com/Chi-SquaredDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Chi-squared_distribution
        [3]: scipy.stats.distributions
        """
        if k < 0 or type(k) != int:
            raise ValueError('k must be a positive iteger')
        self.k = k
        self.support = '[0, inf)'
        self.mean = k
        self.median = k * (1 - 2 / (9 * k)) ** 3
        self.mode = max(k - 2, 0)
        self.variance = 2 * k
        self.skewness = sqrt(8. / k)
        self.ex_kurtosis = 12. / k


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|k) =(1 / (2**(k/2) * gamma(k/2))) * x**(k / 2 - 1) * exp(-x/2)

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
        if (x<0).any():
            raise ValueError('at least one value of x is not in the support of \
                             the dist. X must be non-negative.')
        k = self.k
        pdf = (1. / (2 ** (k / 2) * gamma(k / 2.))) * \
                    x ** (k / 2. - 1.) * np.exp(- x / 2.)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|k) = gammainc(k/2, x/2) / gamma(k/2)

        Where gammainc and gamma are the incomplete gamma and gamma functions,
        respectively.

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
        cdf = chdtr(self.k, x)

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
        draw = np.random.chisquare(self.k, n)

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
        ppf = chdtri(self.k, 1. - x)

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
        plt.title(r'$\chi^2$ (%.1f): PDF from %.2f to %.2f' %(self.k, low,  high))
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
        plt.title(r'$\chi^2$ (%.1f): PDF from %.2f to %.2f' %(self.k, low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([1.2, 1.5, 2.1, 5.4])
    x2 = np.array([.1, .3, .5, .9])
    k = 4
    chi2 = Chi_square(k)
    print 'support = ', chi2.support
    print 'mean = ', chi2.mean
    print 'median= ', chi2.median
    print 'mode = ', chi2.mode
    print 'variance = ', chi2.variance
    print 'skewness = ', chi2.skewness
    print 'Excess kurtosis = ', chi2.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', chi2.pdf(x)
    print 'cdf at x = ', chi2.cdf(x)
    print 'ppf at x = ', chi2.ppf(x2)
    print 'sf at x = ', chi2.sf(x)
    print '6 random_draws ', chi2.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 10)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 10)
    chi2.plot_pdf(0, 10)
    chi2.plot_cdf(0, 10)
