import logging
from abc import ABC, abstractmethod

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import *
from sklearn.model_selection import train_test_split
import logging
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

class Model(ABC):

    """Abstract class for models
    """

    @abstractmethod
    def train(self, X_train, y_train):
        """
        train the model
        Args:
            X_train : training data
            y_train : training labels

        Returns:
            None
        """
        pass


class Splitter:
    """
    Class for splitting data
    
    """
    def __init__(self, data : pd.DataFrame, strategy : str, column :str):
        self.data = data
        self.strategy = strategy
        self.column = column
    
    def handle_split(self, split_size : int) -> Tuple[pd.DataFrame,pd.DataFrame] | None:

        """
        Common function to handle splitting operation
        Args:
        split_size : float -> percentage of train data
        Returns:
        training_split : Tuple[pd.DataFrame,pd.DataFrame] -> split data.
        """

        
        try:
            if self.strategy == "random split":
                y = self.data[[self.column]]
                self.data.drop([self.column],axis = 1, inplace=True)
                x_train,y_train = self._random_split(self.data,y, split_size)
                return x_train, y_train
            else:
                pass
        except Exception as e:
            raise Exception(f"error at Splitter {e}")

    def _random_split(self ,data , y ,split_size):
        """
        function to perform normal train_test split
        """
        x_train,x_test,y_train,y_test = train_test_split(data,y,test_size= 1 - split_size, shuffle=True)
        return x_train,y_train


class LinearReg(Model):

    """
    Model
    """ 
    def train(self, X_train, y_train, **kwargs):
        """
        train the model
        Args:
            X_train : training data
            y_train : training labels

        Returns:
            None
        """
        try:
            reg = LinearRegression(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Model trained!")
            return reg

        except Exception as e:
            logging.error("Error in training model: {e}")
            raise e
        

class RidgeReg(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            reg = Ridge(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Model trained!")
            return reg
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class LassoReg(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            reg = Lasso(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Model trained!")
            return reg
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class DecisionTreeReg(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            reg = DecisionTreeRegressor(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Model trained!")
            return reg
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class RandomForestReg(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            reg = RandomForestRegressor(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Model trained!")
            return reg
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e
        
class LogisticReg(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            clf = LogisticRegression(**kwargs)
            clf.fit(X_train, y_train)
            logging.info("Model trained!")
            return clf
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class DecisionTreeCls(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            clf = DecisionTreeClassifier(**kwargs)
            clf.fit(X_train, y_train)
            logging.info("Model trained!")
            return clf
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class RandomForestCls(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            clf = RandomForestClassifier(**kwargs)
            clf.fit(X_train, y_train)
            logging.info("Model trained!")
            return clf
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class GradientBoostingCls(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            clf = GradientBoostingClassifier(**kwargs)
            clf.fit(X_train, y_train)
            logging.info("Model trained!")
            return clf
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class SVCCls(Model):
    def train(self, X_train, y_train, **kwargs):
        try:
            clf = SVC(**kwargs)
            clf.fit(X_train, y_train)
            logging.info("Model trained!")
            return clf
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e
        
class KMeansClus(Model):
    def train(self, X_train, **kwargs):
        try:
            clus = KMeans(**kwargs)
            clus.fit(X_train)
            logging.info("Model trained!")
            return clus
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class DBSCANClus(Model):
    def train(self, X_train, **kwargs):
        try:
            clus = DBSCAN(**kwargs)
            clus.fit(X_train)
            logging.info("Model trained!")
            return clus
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e

class AgglomerativeClus(Model):
    def train(self, X_train, **kwargs):
        try:
            clus = AgglomerativeClustering(**kwargs)
            clus.fit(X_train)
            logging.info("Model trained!")
            return clus
        except Exception as e:
            logging.error(f"Error in training model: {e}")
            raise e
        