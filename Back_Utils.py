import streamlit as st
from src.data_cleaning import *
import pandas as pd
from typing import List

# @st.cache_data
def drop_column(column: List[str], data : pd.DataFrame) -> pd.DataFrame:

    drop_data = DataDrop(data)
    data = drop_data.handle_data(column)

    return data

# @st.cache_data
def impute_columns(columns : List[str], data : pd.DataFrame, strategy: str, impute_parameters : dict) -> pd.DataFrame:

    impute = Imputer(data)

    for column in columns:
        data = impute.handle_data(column, strategy, impute_parameters["strategy"],impute_parameters["fill_value"])

    return data
