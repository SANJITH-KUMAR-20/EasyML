import logging

from src.data_cleaning import DataPrep, DataPreprocessStrategy, DataSplitStrategy
import pandas as pd
from zenml import step
from typing import Tuple
from typing_extensions import Annotated

@step
def clean_data(data : pd.DataFrame = None) -> Tuple[
    Annotated[pd.DataFrame, "x_train"],
    Annotated[pd.DataFrame, "x_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"]
]:

    """
    Cleans the input data based on the given
    -----------------------------------------
    Args: 
        raw data
    Returns:
        x_train: Training data
        x_test: Testing data
        y_train: Training label
        y_test: Testing label
    """

    try:
        process_strategy = DataPreprocessStrategy()
        data_cleaning = DataPrep(data, process_strategy)
        processed_data = data_cleaning.handle_data()

        divide_strategy = DataSplitStrategy()
        data_cleaning = DataPrep(processed_data, divide_strategy)
        x_traain, x_test, y_train, y_test = data_cleaning.handle_data()

        logging.info("Cleaning and Splitting Successful...")
    
    except Exception as e:
        logging.error(f"Error encountered {e}")
        raise e
           