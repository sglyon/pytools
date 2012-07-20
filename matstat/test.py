"""
Created July 19, 2012

Author: Spencer Lyon
7-19-12:
    Tested lognorm, norma, beta, chi, chi_square, exponential, f_dist, gamma
    Results: all functioning properly.
"""
from lognorm import Lognorm
from normal import Normal
from beta import Beta
from chi import Chi
from chi_square import Chi_square
from exponential import Exponential
from f_dist import F_dist
from gamma import Gamma
from numpy import array

x = array([1.2, 1.5, 2.1, 5.4])
x2 = array([.1, .3, .4, .7])

mu, sigma, alpha, beta, k, gamma, d1, d2, kk, theta = [1.2, 2.3, .4, .5, 4,
                                                       3, 4, 6, 1.6, .7]

lnorm = Lognorm(mu, sigma)
norm = Normal(mu, sigma)
beta = Beta(alpha, beta)
chi = Chi(k)
chi2 = Chi_square(k)
exp = Exponential(gamma)
f = F_dist(d1, d2)
gamma = Gamma(kk, theta)

print 'lnorm.cdf(x): ', lnorm.cdf(x)
print 'norm.cdf(x): ', norm.cdf(x)
print 'beta.cdf(x2): ', beta.cdf(x2)
print 'chi.cdf(x): ', chi.cdf(x)
print 'chi2.cdf(x): ', chi2.cdf(x)
print 'exp.cdf(x): ', exp.cdf(x)
print 'f.cdf(x): ', f.cdf(x)
print 'gamma.cdf(x): ', gamma.cdf(x)

print 'lnorm.pdf(x): ', lnorm.pdf(x)
print 'norm.pdf(x): ', norm.pdf(x)
print 'beta.pdf(x2): ', beta.pdf(x2)
print 'chi.pdf(x): ', chi.pdf(x)
print 'chi2.pdf(x): ', chi2.pdf(x)
print 'exp.pdf(x): ', exp.pdf(x)
print 'f.pdf(x): ', f.pdf(x)
print 'gamma.pdf(x): ', gamma.pdf(x)

