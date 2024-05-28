from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, LabelEncoder, MinMaxScaler
from abc import ABC, abstractmethod
import typing
import logging
import numpy as np
from typing import *
import pandas as pd
from sklearn.base import *

# enable_iterative_imputer()
class DataStrategy(ABC):

    """
    Abstract class defining stratgy for handling data
    """

    @abstractmethod
    def handle_data(self, data: pd.DataFrame = None) -> typing.Union[pd.DataFrame, pd.Series]:
        pass


class Scaler(DataStrategy):
    
    """
    class for handling data scaling and encoding.
    """
    def __init__(self, data : pd.DataFrame, strategy : typing.Literal["Standard Scaler", "MinMax Scaler"]) -> None:
        super(DataStrategy, self).__init__()
        self.data = data
        self.strategy = strategy

    def _standard_scaler(self, columns : List[str],parameter) -> pd.DataFrame:
        scaler = StandardScaler()
        try:
            self.data[columns] = scaler.fit_transform(self.data[columns])
            return self.data
        except Exception as e:
            raise e
        
    def _minmax_scaler(self, columns : List[str], parameter) -> pd.DataFrame:
        scaler = MinMaxScaler()
        if parameter.parameters and parameter.parameters["feature_range"]:
            scaler = MinMaxScaler(parameter.parameters["feature_range"])
        try:
            self.data[columns] = scaler.fit_transform(self.data[columns])
            return self.data
        except Exception as e:
            raise e
        
    def handle_data(self, column : List[str], parameter) -> pd.DataFrame | pd.Series:
        if self.strategy == "MinMax Scaler":
            return self._minmax_scaler(column, parameter)
        elif self.strategy == "Standard Scaler":
            return self._standard_scaler(column,parameter)
        else:
            logging.error("No such strategy")

    
class Encoding(DataStrategy):

    def __init__(self, data  : pd.DataFrame, strategy : typing.Literal["OrdinalEncoder", "OneHotEncoder", "LabelEncoder"]) -> None:
        super(Encoding, self).__init__()
        self.data = data
        self.strategy = strategy
        
    def _onehot_encoding(self, column : List[str]) -> pd.DataFrame:
        encoding = OneHotEncoder()
        try:
            data = encoding.fit_transform(self.data[column])
            self.data.drop(column, axis=1)
            self.data = pd.concat([self.data,data], axis= 1)
            return self.data
        except Exception as e:
            raise e
        
    def _ordinal_encoding(self, column : List[str]) -> pd.DataFrame:
        encoding = OrdinalEncoder()
        try:
            self.data[column] = encoding.fit_transform(self.data[column])
            return self.data
        except Exception as e:
            raise e

    def _label_encoding(self, column : List[str]) -> pd.DataFrame:
        encoding = LabelEncoder()
        try:
            self.data[column] = encoding.fit_transform(self.data[column])
            return self.data
        except Exception as e:
            raise e  
        
    def handle_data(self, parameter) -> pd.DataFrame | pd.Series:
        
        if self.strategy == "OneHot Encoding":
            return self._onehot_encoding(parameter.columns)
        
        elif self.strategy == "Label Encoding":
            return self._label_encoding(parameter.columns)
        
        elif self.strategy == "Ordinal Encoding":
            return self._ordinal_encoding(parameter.columns)
        
        else:
            logging.error("No such strategy")
    
    

