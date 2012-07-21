"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt
import numpy as np
from scipy.special import beta, fdtr, fdtri
import matplotlib.pyplot as plt

class F_dist:
    def __init__(self, d1=1, d2=2):
        """
        Initializes an object of F distribution type. We instantiate the
        object as well as some common statistics about it. This will make sure
        d1 and d2 have acceptable values and raise a ValueError if either
        doesn't.

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
        [1]: www.http://mathworld.wolfram.com/F-Distribution.html
        [2]: www.http://en.wikipedia.org/wiki/F-distribution
        [3]: scipy.stats.distributions
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
        pdf = np.sqrt(((d1 * x) ** d1 * (d2**d2)) / (d1 * x + d2)**(d1 + d2))/ \
                (x * beta (d1 / 2., d2 / 2.))
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|d1, d2) = I_{(d1 * x) / (d1 * x + d2)} (d1 / 2, d2 / 2)

        where I_stuff is the regularized incomplete beta function.

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
        plt.title('F(%.1f, %.1f): PDF from %.2f to %.2f' %(self.d1, self.d2,
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
        plt.title('F(%.1f, %.1f): CDF from %.2f to %.2f' %(self.d1, self.d2,
                                                           low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([.1, .3, .4, .7])
    d1 = 4
    d2 = 6
    f = F_dist(d1, d2)
    print 'support = ', f.support
    print 'mean = ', f.mean
    print 'median= ', f.median
    print 'mode = ', f.mode
    print 'variance = ', f.variance
    print 'skewness = ', f.skewness
    print 'Excess kurtosis = ', f.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', f.pdf(x)
    print 'cdf at x = ', f.cdf(x)
    print '6 random_draws ', f.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 3)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 3)
    f.plot_pdf(0, 3)
    f.plot_cdf(0, 3)
