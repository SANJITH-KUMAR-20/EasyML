import logging
from abc import ABC, abstractmethod

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

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