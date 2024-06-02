import streamlit as st
from src.data_cleaning import *
from src.data_scaling import *
from src.model_dev import *
import pandas as pd
from src.config.dataset_man_config import *
from typing import List
from src.utils.sql import *


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

def split(parameter : SplittingRequest, data : pd.DataFrame):
    splitter = Splitter(data,parameter.strategy,parameter.y_column)
    x_train, y_train = splitter.handle_split(parameter.train_test_split)
    return x_train,y_train

def train(parameter: TrainRequest, cursor):
    x_train, y_train = get_data(cursor, parameter.dataset_name)
    
    if parameter.type == "Regression":
        if parameter.strategy == "linearreg":
            mod = LinearReg()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "ridgereg":
            mod = RidgeReg()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "lassoreg":
            mod = LassoReg()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "decisiontreereg":
            mod = DecisionTreeReg()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "randomforestreg":
            mod = RandomForestReg()
            mod.train(x_train, y_train, **parameter.parameters)

    elif parameter.type == "Classification":
        if parameter.strategy == "logisticreg":
            mod = LogisticReg()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "decisiontreecls":
            mod = DecisionTreeCls()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "randomforestcls":
            mod = RandomForestCls()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "gradientboostingcls":
            mod = GradientBoostingCls()
            mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "svmcls":
            mod = SVCCls()
            mod.train(x_train, y_train, **parameter.parameters)

    elif parameter.type == "Clustering":
        if parameter.strategy == "kmeans":
            mod = KMeansClus()
            mod.train(x_train, **parameter.parameters)
        elif parameter.strategy == "dbscan":
            mod = DBSCANClus()
            mod.train(x_train, **parameter.parameters)
        elif parameter.strategy == "agglomerative":
            mod = AgglomerativeClus()
            mod.train(x_train, **parameter.parameters)

    return mod