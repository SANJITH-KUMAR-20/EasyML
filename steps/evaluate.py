import logging

from zenml import step 
import pickle
import pandas as pd

@step
def evaluate_model(df: pd.DataFrame = None)->None:

    """
    Evaluates a model on the given data:
    -------------------------------------
    Args: df -> pd.DataFrame (test_data)
    
    """
    pass