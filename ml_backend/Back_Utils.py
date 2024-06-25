import streamlit as st
from src.data_cleaning import *
from src.data_scaling import *
from src.model_dev import *
import pandas as pd
from src.config.dataset_man_config import *
from typing import List
from sklearn.base import RegressorMixin, ClassifierMixin, ClusterMixin
from src.utils.sql import *
from src.evaluation import *


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
    x_train, y_train, x_test, y_test = splitter.handle_split(parameter.train_test_split)
    return x_train,y_train, x_test, y_test

def train(parameter: TrainRequest, engine):
    x_train, y_train = get_data(engine, parameter.dataset_name)
    
    if parameter.type == "Regression":
        if parameter.strategy == "linearreg":
            mod = LinearReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "ridgereg":
            mod = RidgeReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "lassoreg":
            mod = LassoReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "decisiontreereg":
            mod = DecisionTreeReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "randomforestreg":
            mod = RandomForestReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)

    elif parameter.type == "Classification":
        if parameter.strategy == "logisticreg":
            mod = LogisticReg()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "decisiontreecls":
            mod = DecisionTreeCls()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "randomforestcls":
            mod = RandomForestCls()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "gradientboostingcls":
            mod = GradientBoostingCls()
            mod = mod.train(x_train, y_train, **parameter.parameters)
        elif parameter.strategy == "svmcls":
            mod = SVCCls()
            mod = mod.train(x_train, y_train, **parameter.parameters)

    elif parameter.type == "Clustering":
        if parameter.strategy == "kmeans":
            mod = KMeansClus()
            mod = mod.train(x_train, **parameter.parameters)
        elif parameter.strategy == "dbscan":
            mod = DBSCANClus()
            mod = mod.train(x_train, **parameter.parameters)
        elif parameter.strategy == "agglomerative":
            mod = AgglomerativeClus()
            mod = mod.train(x_train, **parameter.parameters)

    return mod

def evaluate(kind : str, model : Union[RegressorMixin, ClassifierMixin, ClusterMixin],data : Tuple[pd.DataFrame]) -> Dict[str,float]:

    x_test, y_test = data[0], data[1]

    y_pred = model.predict(x_test)
    y_test = np.squeeze(y_test.to_numpy())
    y_pred = np.squeeze(y_pred)

    if kind == "regression":
        mse = MSE().calculate_scores(y_test,y_pred)
        mae = MAE().calculate_scores(y_test,y_pred)
        r2 = R2().calculate_scores(y_test,y_pred)
        return {"r2" : r2,"mae" : mae,"mse" : mse}
    
    elif kind == "classification":
        acc = Accuracy().calculate_scores(y_test,y_pred)
        prec = Precision().calculate_scores(y_test,y_pred)
        f1 = F1().calculate_scores(y_test,y_pred)
        recall = Recall().calculate_scores(y_test,y_pred)
        return {"accuracy" : acc, "prec" : prec,"f1" : f1,"recall" : recall}
    
    elif kind == "clustering":
        pass

    else:
        raise Exception("No such Method")  
