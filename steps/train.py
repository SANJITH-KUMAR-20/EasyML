import logging

import mlflow
from zenml import step
from zenml.client import Client

import pandas as pd
from sklearn.base import RegressorMixin

from .config import ModelNameConfig
from src.model_dev import LinearReg

experiment_tracker = Client().active_stack.experiment_tracker

@step(experiment_tracker = experiment_tracker.name, enable_cache= False)
def train_model(X_train: pd.DataFrame,
                X_test: pd.DataFrame,
                y_train: pd.DataFrame,
                y_test: pd.DataFrame,
                config: ModelNameConfig) -> RegressorMixin:
    """
    Trains the model
    ------------------
    Args : df (input_data -> pd.DataFrame)
    """ 
    try:
        model = None
        if config.model_name == "LinearRegression":
            mlflow.sklearn.autolog()
            model = LinearReg()
            trained_model = model.train(X_train, y_train)
            return trained_model
        else:
            raise ValueError("Model {} not supported".format(config.model_name))
    except Exception as e:
        logging.error(f"Error in training model: {e}")
        raise e
    