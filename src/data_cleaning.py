import logging
from abc import ABC, abstractmethod

from typing import List
import numpy as np
from typing import Union
import pandas as pd
from pandas.core.api import Series as Series
# from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split
from sklearn.impute import *
from sklearn.base import *
# from sklearn.experimental import enable_iterative_imputer

# enable_iterative_imputer()
class DataStrategy(ABC):

    """
    Abstract class defining stratgy for handling data
    """

    @abstractmethod
    def handle_data(self, data: pd.DataFrame = None) -> Union[pd.DataFrame, pd.Series]:
        pass


class Imputer(DataStrategy):

    """Class for Imputing missing values"""

    def __init__(self,data: pd.DataFrame):
        self.data = data
        self.data.fillna(np.nan)


    def handle_data(self,column : str | list,Impute_Strategy : str = "Simple_Imputer", strategy : str = "mean", constant : int | str |float = None, n_nearest_features : int = None
                    ,weights : str = "uniform") -> pd.DataFrame | pd.Series:
        
        """
        function for imputation
        """
        if self.data.empty:
            raise Exception(ValueError)
        if Impute_Strategy == "Simple_Imputer":
            if strategy == "constant" and not constant:
                raise Exception(f"Enter the constant Value")
            self._simple_impute(column, strategy, constant)
        # elif Impute_Strategy == "Iterative_Imputer":
        #     if not strategy == "constant" and constant:
        #         raise Exception(f"Enter the constant Value")
        #     self._iterative_imputer(column, strategy, constant, n_nearest_features)
        elif Impute_Strategy == "KNN_Imputer":
            if not n_nearest_features:
                raise Exception(f"Enter the n_nearest_features")
            self._knn_imputer(column, weights, n_nearest_features)
        else:
            raise Exception("No Such Impute Strategy")
        
        return self.data

    def _simple_impute(self, column : str, strategy : str = "mean", constant : str | int | float = None) -> None:

        imputer = SimpleImputer(missing_values= np.nan, strategy= strategy, fill_value= constant)
        try:
            self.data[column] = imputer.fit_transform(self.data[[column]])
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
        
    # def _iterative_imputer(self, column : str, initial_strategy : str = "mean", constant : str | int |float = None, nn_features : int = None) -> None:
        
    #     imputer = IterativeImputer(missing_values= np.nan, initial_strategy=initial_strategy, fill_value = constant, n_nearest_features= nn_features)
    #     try:
    #         self.data[column] = imputer.fit_transform(self.data["column"])
    #     except Exception as e:
    #         logging.error(f"Error: {e}")
    #         raise e
        
    def _knn_imputer(self, column : str, weights : str = "uniform", n_nearest_neigbours : int = 5) -> None:

        imputer = KNNImputer(missing_values= np.nan, weights= weights, n_neighbors= n_nearest_neigbours)
        try:
            self.data[column] = imputer.fit_transform(self.data[[column]])
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e


class DataDrop(DataStrategy):

    """
    Class for dropping columns
    """

    def __init__(self,data: pd.DataFrame):
        self.data = data

    def handle_data(self, columns: list) -> pd.DataFrame | pd.Series:
        
        try:
            data = self.data.drop(columns, axis = 1)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
    
        return data
    
            

    

class DataPreprocessStrategy(DataStrategy):



    def handle_data(self, data: pd.DataFrame = None) -> pd.DataFrame | pd.Series:
        """
        Processing Data
        """
        logging.info("Preprocessing data....")
        try:
            data = data.drop(
                [
                    "order_approved_at",
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date",
                    "order_purchase_timestamp"
                ],
                axis = 1
            )
            data["product_weight_g"].fillna(data["product_weight_g"].median(), inplace=True)
            data["product_length_cm"].fillna(data["product_length_cm"].median(), inplace=True)
            data["product_height_cm"].fillna(data["product_height_cm"].median(), inplace=True)
            data["product_width_cm"].fillna(data["product_width_cm"].median(), inplace=True)
            data["review_comment_message"].fillna("No review", inplace=True)

            data = data.select_dtypes(include= [np.number])
            data.drop(["customer_zip_code_prefix", "order_item_id"], axis = 1, inplace=True)
            return data
        except Exception as e:
            logging.error(f"Error in processing data: {e}")
            raise e


class DataSplitStrategy(DataStrategy):

    """
    Splits data for train and test
    """

    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame | pd.Series:

        try:

            x = data.drop(["review_score"], axis = 1)
            y = data["review_score"]

            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"Error in processing data: {e}")
            raise e


class DataPrep:

    """Preprocess-Clean-Split-Data"""

    def __init__(self, data: pd.DataFrame = None, strategy: DataStrategy = None):

        """
        Constructor
        ------------
        Args : data -> pd.DataFrame(Data to be processed)
        """

        self.data = data
        self.strategy = strategy

    def handle_data(self) -> Union[pd.DataFrame, pd.Series]:
        """
        Handle Data
        """

        try:
            return self.strategy.handle_data(self.data)

        except Exception as e:
            logging.error("Error while processing data")
            raise e




    