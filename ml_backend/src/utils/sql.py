import mysql
import mysql.connector
import pandas as pd
from typing import *
from mysql.connector import errorcode

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
        names = (dataset_name + "_train_x", dataset_name + "_train_y")
        train_x.to_sql(names[0],engine,if_exists="replace",index=False)
        train_y.to_sql(names[1],engine,if_exists="replace",index=False)
        return names
    except Exception as e:
        raise e
    
def get_data(cursor, datasett_name):
    train_data_names = (datasett_name + "_train_x", datasett_name + "_train_y")
    query = f"SELECT * FROM {train_data_names[0]}"
    query1 = f"SELECT * FROM {train_data_names[1]}"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    x_train = pd.DataFrame(rows, columns=column_names)
    cursor.execute(query1)
    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    y_train = pd.DataFrame(rows, columns=column_names)
    return x_train,y_train
    

