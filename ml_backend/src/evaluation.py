import logging
from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics import (mean_squared_error, r2_score, mean_absolute_error,
                             accuracy_score, precision_score, recall_score, f1_score,
                             adjusted_rand_score, normalized_mutual_info_score, silhouette_score)

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

class Accuracy(Evaluation):
    """Evaluation strategy for Accuracy"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating Accuracy...")
            accuracy = accuracy_score(y_true, y_pred)
            logging.info(f"Successfully Calculated Accuracy -> {accuracy}")
            return accuracy
        except Exception as e:
            logging.error(f"Accuracy calculation failed due to {e}")
            raise e

class Precision(Evaluation):
    """Evaluation strategy for Precision"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating Precision...")
            precision = precision_score(y_true, y_pred, average='weighted')
            logging.info(f"Successfully Calculated Precision -> {precision}")
            return precision
        except Exception as e:
            logging.error(f"Precision calculation failed due to {e}")
            raise e

class Recall(Evaluation):
    """Evaluation strategy for Recall"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating Recall...")
            recall = recall_score(y_true, y_pred, average='weighted')
            logging.info(f"Successfully Calculated Recall -> {recall}")
            return recall
        except Exception as e:
            logging.error(f"Recall calculation failed due to {e}")
            raise e

class F1(Evaluation):
    """Evaluation strategy for F1 Score"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating F1 Score...")
            f1 = f1_score(y_true, y_pred, average='weighted')
            logging.info(f"Successfully Calculated F1 Score -> {f1}")
            return f1
        except Exception as e:
            logging.error(f"F1 Score calculation failed due to {e}")
            raise e

class ARI(Evaluation):
    """Evaluation strategy for Adjusted Rand Index"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating Adjusted Rand Index...")
            ari = adjusted_rand_score(y_true, y_pred)
            logging.info(f"Successfully Calculated Adjusted Rand Index -> {ari}")
            return ari
        except Exception as e: 
            logging.error(f"Adjusted Rand Index calculation failed due to {e}")
            raise e

class NMI(Evaluation):
    """Evaluation strategy for Normalized Mutual Information"""
    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        try:
            logging.info("Calculating Normalized Mutual Information...")
            nmi = normalized_mutual_info_score(y_true, y_pred)
            logging.info(f"Successfully Calculated Normalized Mutual Information -> {nmi}")
            return nmi
        except Exception as e:
            logging.error(f"Normalized Mutual Information calculation failed due to {e}")
            raise e

class Silhouette(Evaluation):
    """Evaluation strategy for Silhouette Score"""
    
    def calculate_scores(self, X: np.ndarray, labels: np.ndarray) -> float:
        try:
            logging.info("Calculating Silhouette Score...")
            silhouette = silhouette_score(X, labels)
            logging.info(f"Successfully Calculated Silhouette Score -> {silhouette}")
            return silhouette
        except Exception as e:
            logging.error(f"Silhouette Score calculation failed due to {e}")
            raise e
