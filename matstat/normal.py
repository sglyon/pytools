"""
Created July 19, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import exp, pi, sqrt
from scipy.special import erf, ndtri
import matplotlib.pyplot as plt

class Normal:
    def __init__(self, mu = 0, sigma = 1.):
        """
        Initializes an object of Normal distribution type. We instantiate the
        object as well as some common statistics about it. This will also
        make sure mu and sigma have acceptable values and raise a ValueError if
        they don't.

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
        [1]: www.http://mathworld.wolfram.com/PoissonProcess.html
        [2]: www.http://en.wikipedia.org/wiki/Normal_distribution
        [3]: scipy.stats.distributions
        """
        if sigma <= 0:
            raise ValueError(" Standard Deviation must be positive")
        else:
            self.support = '(-inf, inf)'
            self.mu = mu
            self.sigma = sigma
            self.mean = mu
            self.stdev = sigma
            self.variance = sigma ** 2
            self.skewness = 0.0
            self.ex_kurtosis = 0.0
            self.median = mu
            self.mode = mu


    def pdf(self, x):
        """
        Computes the probability density function of the normal distribution
        at the point x. The pdf is defined as follows:
            f(x|mu, sigma) = 1/sqrt(2 * pi * sigma ** 2) * \
                             exp( - ((x - mu) / (sqrt(2) * sigma)) ** 2)

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
        coef = 1. / (self.stdev * root_2_pi)
        pdf = np.exp( - ((x - self.mean) / (sqrt(2) * self.stdev)) ** 2)
        pdf *= coef

        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the normal
        distribution at the point(s) x. The cdf is defined as follows:
            F(x|mu, sigma) = 1 / 2 * (1 + erf((x - mu)/ (sigma * sqrt(2))))

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
        cdf = 1 / 2. * (1 + erf((x - self.mean) / (self.stdev * sqrt(2))))

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
        draw = np.random.randn(n)
        draw = draw * self.stdev + self.mean

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
        ppf = ndtri(x)

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
        plt.title('N(%.1f, %.1f): PDF from %.2f to %.2f' %(self.mu,
                                                              self.sigma,
                                                              low,  high))
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
        x = np.linspace(low, high, 400)
        plt.figure()
        plt.plot(x, self.cdf(x))
        plt.title('N(%.1f, %.1f): PDF from %.2f to %.2f' %(self.mu,
                                                              self.sigma,
                                                              low,  high))
        plt.axhline(color='k')
        plt.axvline(color='k')
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([.1, .3, .4, .7])
    mu = 0.
    sigma = 1.
    norm = Normal(mu, sigma)
    print 'support = ', norm.support
    print 'mean = ', norm.mean
    print 'median= ', norm.median
    print 'mode = ', norm.mode
    print 'variance = ', norm.variance
    print 'skewness = ', norm.skewness
    print 'Excess kurtosis = ', norm.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', norm.pdf(x)
    print 'cdf at x = ', norm.cdf(x)
    print 'ppf at x = ', norm.ppf(x)
    print 'sf at x = ', norm.sf(x)
    print '6 random_draws ', norm.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (-3, 3)
    print 'Plot of cdf from %.2f to %.2f ' % (-3, 3)
    norm.plot_pdf(-3, 3)
    norm.plot_cdf(-3, 3)
