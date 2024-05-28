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
    data = impute.handle_data(parameter=parameter)

    return data


def encode(parameter : EncodeRequest, data : pd.DataFrame):
    encode = Encoding(data, parameter.strategy)
    data = encode.handle_data(parameter)
    return data


def standardize(parameter : StandardizeRequest, data : pd.DataFrame):

    standardize = Scaler(data, parameter.strategy)
    data = standardize.handle_data(parameter.columns, parameter)

    return data
