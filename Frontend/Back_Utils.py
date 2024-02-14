import streamlit as st
# from src.data_cleaning import *
import pandas as pd

@st.cache_data
def drop_column(column: list, data : pd.DataFrame) -> pd.DataFrame:

    drop_data = DataDrop(data)
    data = drop_data.handle_data(column)

    return data
