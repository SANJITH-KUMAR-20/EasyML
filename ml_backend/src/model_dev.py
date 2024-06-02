import logging
from abc import ABC, abstractmethod

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import *
from sklearn.model_selection import train_test_split

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