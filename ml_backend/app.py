from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import *
from pydantic import BaseModel
import os
from src.tests.testroutes import *
from src.config.dataset_man_config import *
from src import DataObject
import pandas as pd
from Back_Utils import *
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from io import StringIO
import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine



class ManipulateRequest(BaseModel):
   columns : List[str]
   strategy : str
   content : Optional[int]

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "null"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host = "localhost"
user = "root"
password = "$@njith2003"
database = 'mynewdatabase'
password = quote_plus(password)

db_config = {
    'user': 'root',
    'password': '$@njith2003',
    'host': 'localhost',
    'database': 'mynewdatabase'
}

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{database}"

engine = create_engine(DATABASE_URL)

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), name: str = "dummy", type: str = "csv"):
    try:
        dir = "../database"
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        if type == "csv":
            file_path = f"{dir}/{name}.csv"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            data = pd.read_csv(file_path)
            
            data.to_sql(name, con=engine, if_exists='replace', index=False)
            
            return {"message": "success!"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    
@app.get("/download-table/{table_name}")
async def download_table_as_csv(table_name: str):
    try:

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        connection.close()
        df = pd.DataFrame(rows, columns=column_names)
        df = df.to_csv()

        return Response(content=df, media_type="application/json")

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-data/{table_name}")
async def delete_table(table_name:str):

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        connection.commit()
        cursor.close()
        connection.close()

        return {"data deleted successfully"}
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/drop-column")
def drop_column(para : DropColumnsRequest):

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        drop_cols = ", ".join(f"DROP COLUMN {col}" for col in para.columns)
        query = f"ALTER TABLE {para.table_name} {drop_cols}"

        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        return {"column dropped successfully"}
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/impute-data")
def impute_data(config : ImputeRequest):

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM {config.table_name}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        connection.close()
        df = pd.DataFrame(rows, columns=column_names)

        data = impute_columns(config,df)
        data.to_sql(config.table_name, con=engine, if_exists='replace', index=False)

        return {"imputation successful"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/standardize-data")
def standardize_data(config :StandardizeRequest) -> None:
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM {config.table_name}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        connection.close()
        df = pd.DataFrame(rows, columns=column_names)
        print(df)
        data = standardize(config,df)
        data.to_sql(config.table_name, con=engine, if_exists='replace', index=False)

        return {"scaling successful successful"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=str(e))
    

