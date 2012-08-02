"""
Created August 1, 2012

Author: Spencer Lyon
"""
from numpy import std, mean, zeros, diag, empty, dot
from scipy.linalg import lstsq, inv, svd

def normalize_data(X, Y, intercept=True):
    """
    This function will normalize the data to be used in the regression.
    This typically leads to more stable regression results.
    It is assumed that the regression is set up with X as the independent
    variables, Y as the dependent one, and beta as the coefficients in this way:

        Y = beta0 + x1 * beta1 + x * beta2 + ... xn * betan = X * Beta

    Parameters
    ----------
    X: numpy array, dtype=float, shape= (T x n)
        This is the array of data that comes from the independent variables.
        It is assumed that if an intercept term is included in the regression
        that is is represented in this matrix the first column being 1.

    Y: numpy array, dtype=float, shape = (T x NN)
        This is the dependent variable that is to be regressed. If there is
        more than one column it is assumed that multiple simulatneous
        regressions are to be run.

    intercept: bool, optional(default=True)
        Whether or not an intercept term is included in the regression.

    Returns
    -------
    X1: numpy array, dtype=float, shape=(T x n1)
        The normalized independent variables. n1 is the new number of parameters
        If there is an intercept term it is equal to n - 1. Otherwise it is just
        equal to n.

    Y1: numpy array, dtype-float, shape=(T x NN)
        The normalized dependent variable.
    """
    if intercept == True:
        X1 = (X[:, 1:] - mean(X[:, 1:], axis=0)) / std(X[:, 1:], axis=0, ddof=1)
        Y1 = (Y - mean(Y, axis=0)) / std(Y, axis=0, ddof=1)

    else:
        X1 = (X - mean(X, axis=0)) / std(X, axis=0, ddof=1)
        Y1 = (Y - mean(Y, axis=0)) / std(Y, axis=0, ddof=1)

    return X1, Y1

def OLS(X, Y, normalize=True, intercept=True):
    """
    Does ordinary least squares (OLS) regression of Y onto X.

    Parameters
    ----------
    X: numpy array, dtype=float, shape= (T x n)
        This is the array of data that comes from the independent variables.
        It is assumed that if an intercept term is included in the regression
        that is is represented in this matrix the first column being 1.

    Y: numpy array, dtype=float, shape = (T x NN)
        This is the dependent variable that is to be regressed. If there is
        more than one column it is assumed that multiple simulatneous
        regressions are to be run.

    normalize: boolean, optional(default=True)
        Bool telling whether or not you want to normalize the data before the
        regression starts.

    intercept: bool, optional(default=True)
        Whether or not an intercept term is included in the regression.

    Returns
    -------
    Beta: array, dtype=float, shape=(n x 1)
        The array of coefficients that minimizes the sum of squared errors.
    """
    if normalize:
        X1, Y1 = normalize_data(X, Y, intercept)
        Beta_1 = lstsq(X1, Y1)[0]
        Beta = empty(Beta_1.size + 1)
        Beta[1:] = (1. / std(X[:,1:], ddof=1)) * std(Y, ddof=1) * Beta_1
        Beta[0] = mean(Y) - dot(mean(X[:,1:], axis=0), Beta[1:])


    else:
        X1, Y1, = [X, Y]
        Beta = lstsq(X1, Y1)

    return Beta

def LS_SVD(X, Y, normalize=True, intercept=True):
    """
    Does least squares regression of Y onto X using the singular value
    decomposition of X. In ill-conditioned problems this is a more reliable
    method than standard OLS. In normal problems there is no difference.

    Parameters
    ----------
    X: numpy array, dtype=float, shape= (T x n)
        This is the array of data that comes from the independent variables.
        It is assumed that if an intercept term is included in the regression
        that is is represented in this matrix the first column being 1.

    Y: numpy array, dtype=float, shape = (T x NN)
        This is the dependent variable that is to be regressed. If there is
        more than one column it is assumed that multiple simulatneous
        regressions are to be run.

    normalize: boolean, optional(default=True)
        Bool telling whether or not you want to normalize the data before the
        regression starts.

    intercept: bool, optional(default=True)
        Whether or not an intercept term is included in the regression.

    Returns
    -------
    Beta: array, dtype=float, shape=(n x 1)
        The array of coefficients that minimizes the sum of squared errors.
    """
    if normalize:
        X1, Y1 = normalize_data(X, Y, intercept)
        U, s, Vh = svd(X1, full_matrices=False)
        V = Vh.T
        S_inv = diag(1. / s)
        Beta_1 = dot(dot(dot(V, S_inv), U.T), Y1).squeeze()
        Beta = empty(Beta_1.size + 1)
        Beta[1:] = (1. / std(X[:,1:], ddof=1)) * std(Y, ddof=1) * Beta_1
        Beta[0] = mean(Y) - dot(mean(X[:,1:], axis=0), Beta[1:])

    else:
        X1, Y1, = [X, Y]
        U, s, Vh = svd(X1, full_matrices=False)
        V = Vh.T
        S_inv = diag(1. / s)
        Beta = dot(dot(dot(V, S_inv), U.T), Y1).squeeze()


    return Beta
