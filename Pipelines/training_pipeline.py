import logging

from zenml import pipeline
from steps.ingest_data import ingest_data
from steps.cleaning_data import clean_data
from steps.train import train_model
from steps.evaluate import evaluate_model
from steps.config import ModelNameConfig

@pipeline(enable_cache= True)
def training_pipeline(data_path : str) -> None:
    """
    Takes, cleanes and trains and evaluates th model
    -------------------------------------------------
    Args: data_path -> str(path to the data)
    """
    df = ingest_data(data_path)
    x_train, x_test, y_train, y_test = clean_data(df)
    model = train_model(x_train, x_test, y_train, y_test)
    r2_score, mse = evaluate_model(model, x_test, y_test)
