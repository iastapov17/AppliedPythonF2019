#!/usr/bin/env python
# coding: utf-8


import numpy as np


class LogisticRegression:
    def __init__(self, lambda_coef=0.7, C=2, batch_size=50, max_iter=100):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self._lc = lambda_coef
        self._alpha = 1 / C
        self._batch_size = batch_size
        self._max_iter = max_iter
        self._weight = np.array([])
        self._loss = []

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if X_train.shape[0] != y_train.shape[0]:
            raise AssertionError

        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        rows = X_train.shape[0]
        cols = X_train.shape[1]
        self._weight = np.random.normal(size=cols)
        gt = np.zeros(X_train.shape[1])
        for epoch in range(self._max_iter):
            data = np.hstack((X_train, y_train.reshape((-1, 1))))
            np.random.shuffle(data)
            X_train = data[:, : -1]
            y_train = data[:, -1].flatten()
            for i in np.arange(0, rows, self._batch_size):
                batch = X_train[i:i + self._batch_size]
                y = y_train[i:i + self._batch_size]
                pred = self.predict_proba(batch)
                gradient = ((batch.T @ (pred - y)) / batch.shape[0]) + self._alpha * np.sign(self._weight)
                gt += gradient ** 2
                self._weight -= self._lc * gradient / np.sqrt(gt + 1e-7)
            self._loss.append(self.logloss(y_train, X_train))

    def predict(self, X_test, pr=0.5):
        """
        Predict using model.
        :param pr:
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        prob = self.predict_proba(X_test)
        predictions = np.where(prob >= pr, 1, 0)
        return predictions

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        data = X_test
        if data.shape[1] != self._weight.T.shape[0]:
            data = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return 1 / (1 + np.exp(-(data @ self._weight.T)))

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        return self._weight

    def logloss(self, y, data):
        return -1 * np.sum((y * np.log(self.predict_proba(data))) + ((1 - y) * np.log(1 - self.predict_proba(data))))