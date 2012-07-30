"""
Created July 19, 2012

Author: Spencer Lyon
"""
from __future__ import division
from math import sqrt
import numpy as np
from scipy.special import gamma as Fgamma
from scipy.special import gammainc, gammaincinv
import matplotlib.pyplot as plt


class Gamma:
    """
    This distribution follows the form where k is the shape parameter and theta
    is the scale parameter rather then the alternative where alpha is the shape
    and beta is the rate parameter.

    If you want to pass in the rate you should say that theta= 1 / rate
    """
    def __init__(self, k=.5, theta=.5):
        """
        Initializes an object of gamma distribution type. We instantiate the
        object as well as some common statistics about it. This will make sure
        k and theta have acceptable values and raise a ValueError if either
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
        [1]: www.http://mathworld.wolfram.com/GammaDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Gamma-distribution
        [3]: scipy.stats.distributions
        """
        if k < 0 or theta < 0:
            raise ValueError('k and theta must be positive')
        self.k = k
        self.theta = theta
        self.support = '[0, inf)'
        self.mean = k * theta
        self.median = None
        self.mode = (k - 1) * theta if k >= 1 else None
        self.variance = k * theta ** 2
        self.skewness = 2. / sqrt(k)
        self.ex_kurtosis = 6. / k


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
            f(x|k, theta) =1 / (Fgamma(k) * theta**k) * x**(k-1) * exp(-x/theta)

        Fgamma is the gamma function.

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
        theta = self.theta
        pdf = 1 / (Fgamma(k) * theta ** k) * x ** (k - 1) * np.exp(-x / theta)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|k, theta) = 1 / Fgamma(k) * gammainc(k, x / theta)

        where Fgamma gammainc is the gamma function and incomplete gamma
        function, respectively.

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
        cdf =  gammainc(self.k, x / self.theta)

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
        draw = np.random.standard_gamma(self.k, n) * self.theta

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
        ppf = gammaincinv(self.k, x) * self.theta

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
        plt.title(r'$\Gamma(%.1f, %.1f)$: CDF from %.2f to %.2f' %(self.k,
                                                                  self.theta,
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
        plt.title(r'$\Gamma(%.1f, %.1f)$: CDF from  %.2f to %.2f' %(self.k,
                                                                  self.theta,
                                                                  low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([.1, .3, .4, .7])
    k = 1.6
    theta = 0.7
    gam = Gamma(k, theta)
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
    print 'ppf at x = ', gam.ppf(x)
    print 'sf at x = ', gam.sf(x)
    print '6 random_draws ', gam.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 3)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 3)
    gam.plot_pdf(0, 3)
    gam.plot_cdf(0, 3)
