import logging
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from typing import Tuple

class Evaluation(ABC):

    """Abstract class for evaluation methods"""

    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, float]:
        """
        Calculates the scores for the model

        Args:
            y_true : np.ndarray(true labels)
            y_pred : np.ndarray(predicted labels)

        Returns:
            None
        """
        pass

class MSE(Evaluation):

    """Evaluation strategies(Mean Squared Error)"""

    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating MSE")
            mse = mean_squared_error(y_true, y_pred)
            logging.info(f"Successfully Calculated MSE -> {mse}")
            return mse
        except Exception as e:
            logging.error(f"Metric calculation failed due to {e}")
            raise e    

class R2(Evaluation):

    """
    Evaluation Strategy(R2 Score)
    """

    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating R2 Score...")
            r2 = r2_score(y_true, y_pred)
            logging.info(f"Successfully Calculated R2 score -> {r2}")
            return r2
        except Exception as e:
            logging.error(f"R2 score calculation failed due to {e}")
            raise e
        
class MAE(Evaluation):
    """
    Evaluation Strategy(Mean Absolute Error)
    """


    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating R2 Score...")
            mae = mean_absolute_error(y_true, y_pred)
            logging.info(f"Successfully Calculated R2 score -> {mae}")
            return mae
        except Exception as e:
            logging.error(f"R2 score calculation failed due to {e}")
            raise e
