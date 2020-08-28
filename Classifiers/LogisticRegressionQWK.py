"""
Author: Chris Ormerod

Many of the classifiers we use are based on metrics that do not optimize
quadratic weighted kappa. This package is intended to serve as an alternative
to the package LogisticRegression, and the functions are based on the
functions associated with LogisticRegression. The main difference is that
we do not use the liblinear library, hence, the fit function uses the 
scipy library. This means it is significantly slower to fit, yet just
as fast to predict. 

The usage of the class mimics that of LogisticRegression, hence

clf = LogisticRegressionQWK()
clf.fit(X_train,y_train)
clf.predict(X_test)

To save an instance, use

import joblib

joblib.dump(clf, filename)

The 

"""

from sklearn.base import BaseEstimator 
from sklearn.metrics import cohen_kappa_score
from scipy.optimize import minimize
import numpy as np
from tqdm import tqdm
import pandas as pd

class LogisticRegressionQWK(BaseEstimator):
    
    def __init__(self):
        """
        We initialize the class by allowing the number of saved values it
        has cycled through to be 0. By default the test qwk, when unspecified
        is -1, which is also the minimal value possible.
        """       
        self.values = []
        self.test_qwk = -1
    
    
    def fit(self, X, y, trials = 5):
        """
        Given a matrix, X, which is of shape (N, n_features), we seek to 
        fit a classifier by constructing matrix, A, of size 
        (n_features, n_classes) and an intercept c of size (n_classes) st 
        the combination
        
        preds = XA + c
        
        approximates y via the function argmax. 
        """
        if isinstance(X,pd.DataFrame):
            X = X.values
        
        self.classes = np.unique(y)
        self.n_classes = len(self.classes)
        if self.n_classes < 2:
            raise ValueError("This solver needs samples of at least 2 classes"
                             " in the data, but the data contains only one"
                             " class: %r" % self.classes[0])
        
        self.n_features = X.shape[1]
        for i in tqdm(range(trials)):
            # By randomly selecting the initial conditions, we are more likely 
            # arrive at a uniquely defined gloabal maximum of the QWK.
            self.coeff_ = np.random.rand(self.n_classes*self.n_features + self.n_classes)       

            def func(c):
                # Input into standard minimization algorithms requires a
                # reformulation of the matrix problem into a single
                # n-dimensional array, where n is the number of entries
                # in the matrix + the intercept
            
                coefficient_matrix = np.reshape(c[:-self.n_classes], 
                                                (self.n_features,
                                                 self.n_classes))
                intercept = c[-self.n_classes:]
                N = len(X)
                out = np.matmul(X, coefficient_matrix) + np.array([intercept for _ in range(N)])
                preds = np.argmax(out,-1)
                qwk = cohen_kappa_score(preds, y, weights= 'quadratic')
                # We maximize QWK by minimizing its negative, allowing this
                # function to be used in a standard way.
                return -qwk
            
            # The Powell optimizer, while slow, offered the most rhobust
            # optimization results. Many of the derivative-based methods
            # are inappropriate due to QWK not being differentiable or
            # continuous. 
            res = minimize(fun = func, x0 = self.coeff_,
                           method = 'Powell',
                           options = {'maxiter':20})
            
            # We need to keep track of the best QWK over trials. 
            if -res['fun'] > self.__max_values():
                best_res = res
            self.values.append(-res['fun'])    
            
        self.coeff_ = best_res['x']
        self.coefficient_matrix_ = np.reshape(self.coeff_[:-self.n_classes], 
                                               (self.n_features,
                                                self.n_classes))
        self.intercept_ = self.coeff_[-self.n_classes:]
        self.test_qwk = -best_res['fun']
        
    def __max_values(self):
        # This is a private funciton written to simplify the logic of the
        # trials.
        if len(self.values) == 0:
            return [-1]
        else:
            return max(self.values)
        
    def __output(self, X):
        # This private function, used in predict, predict_proba and 
        # predict_log_proba, performs the linear approximation for preds
        if isinstance(X,pd.DataFrame):
            X = X.values
        N = len(X)
        out = np.matmul(X, self.coefficient_matrix_) + np.array([self.intercept_ for _ in range(N)])
        return out
        
    def predict(self, X):
        """
        Parameters
        ----------
        X : numpy.array
            The matrix of elements to predict.

        Returns
        -------
        list
            A list of the predictions as they appear in self.classes

        """
        out = self.__output(X)
        preds = np.argmax(out,-1)
        return [self.classes[p] for p in preds]
    
    def predict_proba(self, X):
        """
        Parameters
        ----------
        X : TYPE
            The matrix of elements to predict.

        Returns
        -------
        np.array
            The output of this function is a N x n_classes matrix with the 
            probabilities of each class as defined by the softmax of the 
            outputs for each class. 
        """
        out = self.__output(X)
        return np.exp(out)/np.sum(np.exp(out))
    
    def predict_log_proba(self, X):
        """
        Parameters
        ----------
        X : TYPE
            The matrix of elements to predict.

        Returns
        -------
        np.array
            The output of this function is a N x n_classes matrix with the 
            log probabilities of each class.
        """
        return np.log(self.predict_proba(X))