"""
Created July 20, 2012

Author: Spencer Lyon
"""
from __future__ import division
import numpy
import matplotlib.pyplot as plt

class Uniform:
    def __init__(self, a=0, b=1):
        """
        Initializes an object of uniform distribution type. We instantiate the
        object as well as some common statistics about it.

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
        This class is dependent on matplotlib, and numpy.

        References
        ----------
        [1]: www.http://mathworld.wolfram.com/UniformDistribution.html
        [2]: www.http://en.wikipedia.org/wiki/Uniform_distribution_(continuous)
        [3]: scipy.stats.distributions
        """
        self.a = a
        self.b = b
        self.support = (a, b)
        self.mean = 1 / 2 * ( a + b)
        self.median = 1 / 2 * ( a + b)
        self.mode = 'Any value in (%d, %d)' %(a, b)
        self.variance = 1. / 12 * (b - a) ** 2
        self.skewness =  0
        self.ex_kurtosis = - 6. / 5


    def pdf(self, x):
        """
        Computes the probability density function of the distribution
        at the point x. The pdf is defined as follows:
                         /   1 - (b - a), if x el [a,b]
            f(x|a ,b) = |
                         \   0          , else

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
        low = min(self.a, self.b)
        high = max(self.a, self.b)
        if type(x) != numpy.ndarray and type(x) != list:
            x = numpy.array([x])

        pdf = []
        for val in x:
            if val >= low and val <= high:
                pdf_entry = 1 /(high - low)
            else:
                pdf_entry = 0.0
            pdf.append(pdf_entry)

        pdf = numpy.asarray(pdf)
        return pdf


    def cdf(self, x):
        """
        Computes the cumulative distribution function of the
        distribution at the point(s) x. The cdf is defined as follows:
                         /   0, if x < a
            F(x|a ,b) = |
                        |  (x - a) / (b - a), if x el [a,b)
                        |
                         \   1          , if x >= b

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
        low = min(self.a, self.b)
        high = max(self.a, self.b)
        if type(x) != numpy.ndarray and type(x) != list:
            x = numpy.array([x])

        cdf = []
        for val in x:
            if val < low:
                cdf_entry = 0.
            elif val >= low and val < high:
                cdf_entry = (val - low) / (high - low)
            else:
                cdf_entry = 1.
            cdf.append(cdf_entry)

        cdf = numpy.asarray(cdf)
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
        n = int(n)
        low = min(self.a, self.b)
        high = max(self.a, self.b)
        draw = numpy.random.uniform(low, high, n)

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
        low = min(self.a, self.b)
        high = max(self.a, self.b)
        ppf = (high - low) * x + low

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
        x = numpy.linspace(low, high, 300)
        plt.figure()
        plt.plot(x, self.pdf(x))
        plt.title('U(%.1f, %.1f): PDF from %.2f to %.2f' %(self.a, self.b,
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
        x = numpy.linspace(low, high, 400)
        plt.figure()
        plt.plot(x, self.cdf(x))
        plt.title('U(%.1f, %.1f): CDF from %.2f to %.2f' %(self.a, self.b,
                                                           low, high))
        plt.show()

        return


if __name__ == '__main__':
    x = numpy.array([1.2, 1.5, 2.1, 5.4])
    low = .4
    high = 6
    uni = Uniform(low, high)
    print 'support = ', uni.support
    print 'mean = ', uni.mean
    print 'median= ', uni.median
    print 'mode = ', uni.mode
    print 'variance = ', uni.variance
    print 'skewness = ', uni.skewness
    print 'Excess kurtosis = ', uni.ex_kurtosis
    print 'x = ', x
    print 'pdf at x = ', uni.pdf(x)
    print 'cdf at x = ', uni.cdf(x)
    print '6 random_draws ', uni.rand_draw(6)
    print 'Plot of pdf from %.2f to %.2f ' % (low - 1, high + 1)
    print 'Plot of cdf from %.2f to %.2f ' % (low - 1, high + 1)
    uni.plot_pdf(low - 1, high + 1)
    uni.plot_cdf(low - 1, high + 1)
