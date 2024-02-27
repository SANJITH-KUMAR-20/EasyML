import streamlit as st
from src.data_cleaning import *
import pandas as pd
from typing import List

@st.cache_data
def drop_column(column: List[str], data : pd.DataFrame) -> pd.DataFrame:

    drop_data = DataDrop(data)
    data = drop_data.handle_data(column)

    return data
