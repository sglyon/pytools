"""
Created July 19, 2012

Author: Spencer Lyon
"""
import numpy as np
from math import sqrt
from scipy.special import beta as Fbeta
from scipy.special import btdtr, btdtri
import matplotlib.pyplot as plt

class Beta:
    def __init__(self, alpha=.1, beta=.1):
        """
        Initializes an object of beta distribution type. We instantiate the
        object as well as some common statistics about it. This will make sure
        alpha and beta have acceptable values and raise a ValueError if either
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
        [1]: www.http://mathworld.wolfram.com/BetaDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Beta_distribution
        [3]: scipy.stats.distributions
        """
        if alpha < 0 or beta < 0:
            raise ValueError('mean must be non-negative')
        else:
            self.support = (0, 1)
            self.alpha = alpha
            self.beta = beta
            self.mean = alpha / (alpha + beta)
            self.median = None
            self.mode = (alpha - 1) / (alpha + beta - 2) \
                        if (alpha > 1 and beta > 1) else None
            self.variance = alpha * beta / ((alpha + beta ) **2 +
                                            (alpha + beta +1))
            self.skewness = (2 * (beta - alpha ) * sqrt(alpha + beta + 1)) / \
                             ((alpha + beta + 2) * sqrt(alpha * beta))
            self.ex_kurtosis = None


    def pdf(self, x):
        """
        Computes the probability density function of the  beta distribution
        at the point x. The pdf is defined as follows (alpha -> a, beta -> b):
            f(x|a, b) =(x ** (a - 1) * (1 - x) **(b - 1)) / Fbeta(a, b)

        Where Fbeta is the beta function.

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
        alpha = self.alpha
        beta = self.beta
        pdf = (x ** (alpha - 1) * (1 - x) **(beta - 1)) / Fbeta(alpha, beta)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows (where
        alpha->a beta ->b, Fbetainc is incomplete beta function and Fbeta is the
        complete beta function):
            F(x|a, b) = Fbetainc(a, b, x) / Fbeta(a, b)

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
        alpha = self.alpha
        beta = self.beta
        cdf = btdtr(alpha, beta, x)

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
        draw = np.random.beta(self.alpha, self.beta, n)

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
        ppf = btdtri(self.alpha, self.beta, x)

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
        plt.title(r'$\beta$ (%.1f, %.1f): PDF from %.2f to %.2f' %(self.alpha,
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
        plt.title(r'$\beta $ (%.1f, %.1f): PDF from %.2f to %.2f' %(self.alpha,
                                                                self.beta,
                                                                low,  high))
        plt.show()

        return


if __name__ == '__main__':
    x = np.array([.1, .3, .4, .7])
    alpha = .4
    beta = .5
    bet = Beta(alpha, beta)
    print 'support = ', bet.support
    print 'mean = ', bet.mean
    print 'median= ', bet.median
    print 'mode = ', bet.mode
    print 'variance = ', bet.variance
    print 'skewness = ', bet.skewness
    print 'Excess kurtosis = ', bet.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', bet.pdf(x)
    print 'cdf at x = ', bet.cdf(x)
    print '6 random_draws ', bet.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (0, 1)
    print 'Plot of cdf from %.2f to %.2f ' % (0, 1)
    bet.plot_pdf(0, 1)
    bet.plot_cdf(0, 1)
