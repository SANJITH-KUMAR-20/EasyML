import mysql
import mysql.connector
import pandas as pd
from typing import *
from mysql.connector import errorcode
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, case, Column,String,Float
from sqlalchemy.ext.declarative import declarative_base


def setup_connector(host = "localhost",user = "root",password = "$@njith2003",database = 'mynewdatabase'):

    conn = mysql.connector.connect(
    host=host,      # Replace with your host, e.g., "127.0.0.1"
    user=user,   # Replace with your MySQL username
    password=password , # Replace with your database name
    database = database)

    return conn

def databasesetup(database_name : str):

    conn = setup_connector()

    cursor = conn.cursor()
    try:

        cursor.execute(f"CREATE DATABASE {database_name}")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        

def save_splits(engine, dataset_name, splits : Tuple[pd.DataFrame]) -> Tuple[str]:

    try:
        train_x = splits[0]
        train_y = splits[1]
        test_x = splits[2]
        test_y = splits[3]
        names = (dataset_name + "_train_x", dataset_name + "_train_y",dataset_name + "_test_x", dataset_name + "_test_y")
        train_x.to_sql(names[0],engine,if_exists="replace",index=False)
        train_y.to_sql(names[1],engine,if_exists="replace",index=False)
        test_x.to_sql(names[2],engine,if_exists="replace",index=False)
        test_y.to_sql(names[3],engine,if_exists="replace",index=False)
        return names
    except Exception as e:
        raise e
    
def get_data(engine, datasett_name,type = "train"):
    try:
        train_data_names = (datasett_name + f"_{type}_x", datasett_name + f"_{type}_y")
        query = f"SELECT * FROM {train_data_names[0]}"
        query1 = f"SELECT * FROM {train_data_names[1]}"
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            column_names = result.keys()
        x = pd.DataFrame(rows, columns=column_names)
        with engine.connect() as connection:
            result = connection.execute(text(query1))
            rows = result.fetchall()
            column_names = result.keys()
        y = pd.DataFrame(rows, columns=column_names)
        return x,y
    except Exception as e:
        raise e
    
def sort_evaluation_scores(engine,table_name : str, kind : Literal["Regression", "Classification", "Clustering"]) -> None:
    Session = sessionmaker(bind = engine)
    Base = declarative_base()

    class Model(Base):
        __tablename__ = table_name
        model_id = Column(String, primary_key=True)
        model_name = Column(String)
        kind = Column(String)
        total_score = Column(Float)
        mse = Column(Float)
        mae = Column(Float)
        r2 = Column(Float)
        accuracy = Column(Float)
        precision = Column(Float)
        recall = Column(Float)
        f1 = Column(Float)
        ari = Column(Float)
        nmi = Column(Float)
        sil = Column(Float)
        average_score = Column(Float)

    session = Session()

    #Update avergae_score for classification models
    session.query(Model).filter(Model.kind == 'Regression').update({
    Model.average_score: (
        (func.coalesce(Model.mse, 0) + func.coalesce(Model.mae, 0) + func.coalesce(Model.r2, 0)) / 3
    )
    })
    session.commit()

    # Update average_score for classification models
    session.query(Model).filter(Model.kind == 'Classification').update({
        Model.average_score: (
            (func.coalesce(Model.accuracy, 0) + func.coalesce(Model.precision, 0) + func.coalesce(Model.recall, 0) + func.coalesce(Model.f1, 0)) / 4
        )
    })
    session.commit()

    # Update average_score for clustering models
    session.query(Model).filter(Model.kind == 'Clustering').update({
        Model.average_score: (
            (func.coalesce(Model.ari, 0) + func.coalesce(Model.nmi, 0) + func.coalesce(Model.sil, 0)) / 3
        )
    })
    session.commit()

def get_best(engine, table_name : str, kind : Literal["Regression", "Classification", "Clustering"]) -> dict:     
    Session = sessionmaker(bind = engine)
    Base = declarative_base()

    class Model(Base):
        __tablename__ = table_name
        model_id = Column(String, primary_key=True)
        model_name = Column(String)
        kind = Column(String)
        total_score = Column(Float)
        mse = Column(Float)
        mae = Column(Float)
        r2 = Column(Float)
        accuracy = Column(Float)
        precision = Column(Float)
        recall = Column(Float)
        f1 = Column(Float)
        ari = Column(Float)
        nmi = Column(Float)
        sil = Column(Float)
        average_score = Column(Float)

    session = Session()    
    subquery = session.query(
        Model.kind,
        func.max(Model.average_score).label('max_score')
    ).group_by(Model.kind).subquery()

    best_models = session.query(Model).join(
        subquery,
        (Model.kind == subquery.c.kind) & (Model.average_score == subquery.c.max_score)
    ).all()
    result = {}
    for model in best_models:
        result[model.kind] = {
            "model_id" : model.model_id,
            "model_name" : model.model_name,
            "model_score" :  model.average_score
        }

    return result



