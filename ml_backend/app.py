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
import sqlite3
from Back_Utils import *

dataset = {}

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
conn = sqlite3.connect("data.db")

@app.get("/get_csv")
async def get_csv():
    try:
        manipulated_data = pd.read_csv("database/dummy_csv.csv")
        manipulated_data_json = manipulated_data.to_csv()
        return Response(content=manipulated_data_json, media_type="application/json")
    except Exception as e:
        return {"error": str(e)}
   
@app.get("/get_columns")
async def get_columns():
   try:
        data = pd.read_csv("database/dummy_csv.csv")
        columns = ",".join(list(data.columns))
        return Response(content = columns, media_type="application/json")
   except Exception as e:
        return {"error":str(e)}
   
@app.post("/drop_columns")
async def drop_columns(config : DataConfig ):
        if config.dataset_name not in dataset:
            return {"message" : "No such dataset"}
        data = drop_column(config.columns, dataset[config.dataset_name].get_state())
        dataset[config.dataset_name].change_state(data)
        drop_colum(dataset)
        return dataset[config.dataset_name].get_state().head()


@app.post("/upload_csv")
async def get_file(file : UploadFile = File(...),name : str = "dummy", type : str = "csv"):
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
        if name in dataset:
            return {"message" : "DataSet already exists"}
        dataset[name] = DataObject.DataObj(data, name)
        data.to_sql('csv_data', conn, if_exists='replace', index=False)
    return {"message" : "success!"}
   except Exception as e:
      raise e

