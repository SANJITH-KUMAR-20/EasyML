import mysql
import mysql.connector

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
        

