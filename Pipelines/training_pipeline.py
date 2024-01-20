import logging

from zenml import pipeline
from steps.ingest_data import ingest_data
from steps.cleaning_data import clean_data
from steps.train import train_model
from steps.evaluate import evaluate_model

@pipeline(enable_cache= False)
def training_pipeline(data_path : str) -> None:
    """
    Takes, cleanes and trains and evaluates th model
    -------------------------------------------------
    Args: data_path -> str(path to the data)
    """
    df = ingest_data(data_path)
    clean_data(df)
    train_model(df)
    evaluate_model(df)
