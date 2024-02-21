# -*- coding: utf-8 -*-
"""Utility functions for manipulating data
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# Author: Yahya Almardeny <almardeny@gmail.com>
# License: BSD 2 clause

from warnings import warn
from sklearn.utils import check_X_y
from sklearn.utils import check_random_state
from sklearn.utils import check_consistent_length
import numpy as np


def _generate_data(n_inliers, n_outliers, n_features, coef, offset,
                   random_state, n_nan=0, n_inf=0):
    """Internal function to generate data samples.

    Parameters
    ----------
    n_inliers : int
        The number of inliers.

    n_outliers : int
        The number of outliers.

    n_features : int
        The number of features (dimensions).

    coef : float in range [0,1)+0.001
        The coefficient of data generation.

    offset : int
        Adjust the value range of Gaussian and Uniform.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    n_nan : int
        The number of values that are missing (np.NaN). Defaults to zero.

    n_inf : int
        The number of values that are infinite. (np.infty). Defaults to zero.

    Returns
    -------
    X : numpy array of shape (n_train, n_features)
        Data.

    y : numpy array of shape (n_train,)
        Ground truth.
    """

    inliers = coef * random_state.randn(n_inliers, n_features) + offset
    outliers = random_state.uniform(low=-1 * offset, high=offset,
                                    size=(n_outliers, n_features))
    X = np.r_[inliers, outliers]

    y = np.r_[np.zeros((n_inliers,)), np.ones((n_outliers,))]

    if n_nan > 0:
        X = np.r_[X, np.full((n_nan, n_features), np.NaN)]
        y = np.r_[y, np.full((n_nan), np.NaN)]

    if n_inf > 0:
        X = np.r_[X, np.full((n_inf, n_features), np.infty)]
        y = np.r_[y, np.full((n_inf), np.infty)]

    return X, y


def generate_data(n_train=1000, n_test=500, n_features=2, contamination=0.1,
                  train_only=False, offset=10,
                  random_state=None, n_nan=0, n_inf=0):
    """Utility function to generate synthesized data.
    Normal data is generated by a multivariate Gaussian distribution and
    outliers are generated by a uniform distribution.
    "X_train, X_test, y_train, y_test" are returned.
    用于生成合成数据的实用函数。
     正态数据由多元高斯分布生成，
     异常值是由均匀分布生成的。
     返回“X_train、X_test、y_train、y_test”。

    Parameters
    ----------
    n_train : int, (default=1000)
        The number of training points to generate.
        生成的训练数据点

    n_test : int, (default=500)
        The number of test points to generate.
        生成的测试数据点

    n_features : int, optional (default=2)
        The number of features (dimensions).
        特征数（维度）

    contamination : float in (0., 0.5), optional (default=0.1)
        The amount of contamination of the data set, i.e.
        the proportion of outliers in the data set. Used when fitting to
        define the threshold on the decision function.
        数据集的污染量，即
        数据集中异常值的比例。 装配时使用
        定义决策函数的阈值。

    train_only : bool, optional (default=False)
        If true, generate train data only.
        train_only为真时只生成训练数据

    offset : int, optional (default=10)
        Adjust the value range of Gaussian and Uniform.
        调整Gaussian和Uniform的取值范围

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    n_nan : int
        The number of values that are missing (np.NaN). Defaults to zero.
        缺失值的数量 (np.NaN)。 默认为零。

    n_inf : int
        The number of values that are infinite. (np.infty). Defaults to zero.
        值的数量是无限的。 （np.infty）。 默认为零。

    Returns
    -------
    X_train : numpy array of shape (n_train, n_features)
        Training data.

    X_test : numpy array of shape (n_test, n_features)
        Test data.

    y_train : numpy array of shape (n_train,)
        Training ground truth.

    y_test : numpy array of shape (n_test,)
        Test ground truth.

    """

    # initialize a random state and seeds for the instance 初始化实例的随机状态和种子
    random_state = check_random_state(random_state)
    offset_ = random_state.randint(low=offset)
    coef_ = random_state.random_sample() + 0.001  # in case of underflow 如果发生下溢

    n_outliers_train = int(n_train * contamination)  # 用于训练的异常点数量
    n_inliers_train = int(n_train - n_outliers_train)  # 用于训练的正常点数量

    X_train, y_train = _generate_data(n_inliers_train, n_outliers_train,
                                      n_features, coef_, offset_, random_state,
                                      n_nan, n_inf)  # 生成训练特征和训练标签

    if train_only:
        return X_train, y_train  # 只生成训练数据的情况下返回X_train, y_train

    n_outliers_test = int(n_test * contamination)  # 用于测试的异常点数量
    n_inliers_test = int(n_test - n_outliers_test)  # 用于测试的正常点数量

    X_test, y_test = _generate_data(n_inliers_test, n_outliers_test,
                                    n_features, coef_, offset_, random_state,
                                    n_nan, n_inf)  # 生成测试特征和测试标签

    return X_train, X_test, y_train, y_test  # 生成训练和测试数据的情况下返回X_train, X_test, y_train, y_test

