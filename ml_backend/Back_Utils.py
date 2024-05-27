import streamlit as st
from src.data_cleaning import *
from src.data_scaling import *
import pandas as pd
from src.config.dataset_man_config import *
from typing import List


def drop_column(column: List[str], data : pd.DataFrame) -> pd.DataFrame:

    drop_data = DataDrop(data)
    data = drop_data.handle_data(column)

    return data

def impute_columns(parameter : ImputeRequest, data : pd.DataFrame) -> pd.DataFrame:

    impute = Imputer(data)
    print(parameter.parameters["strategy"])
    data = impute.handle_data(parameter=parameter)

    return data


def encode(columns :List[str], data : pd.DataFrame, strategy : str):
    encode = Encoding(data, strategy)
    for column in columns:
        data = encode.handle_data(column)

    return data


def standardize(columns: List[str], data : pd.DataFrame, strategy : str):

    standardize = Scaler(data, strategy)
    for column in columns:
        data = standardize.handle_data(column)

    return data
