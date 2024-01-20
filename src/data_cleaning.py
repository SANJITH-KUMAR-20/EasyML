import logging
from abc import ABC, abstractmethod

import numpy as np
from typing import Union
import pandas as pd
from pandas.core.api import Series as Series
from sklearn.model_selection import train_test_split

class DataStrategy(ABC):

    """
    Abstract class defining stratgy for handling data
    """

    @abstractmethod
    def handle_data(self, data: pd.DataFrame = None) -> Union[pd.DataFrame, pd.Series]:
        pass


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




    