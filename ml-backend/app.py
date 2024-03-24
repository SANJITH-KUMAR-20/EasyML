from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import *
from pydantic import BaseModel
import os
import pandas as pd
import sqlite3



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
        # Read the manipulated data from the local directory
        manipulated_data = pd.read_csv("../data/dummy_csv.csv")
        # Convert the data to JSON format
        manipulated_data_json = manipulated_data.to_json()
        return Response(content=manipulated_data_json, media_type="application/json")
    except Exception as e:
        return {"error": str(e)}
   

@app.post("/upload_csv")
async def get_file(file : UploadFile = File(...), type : str = "csv"):
   try: 
    dir = "../database"
    if not os.path.exists(dir):
        os.mkdir(dir)
    if type == "csv":
        file_path = f"{dir}/dummy_csv.csv"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        data = pd.read_csv(file_path)
        data.to_sql('csv_data', conn, if_exists='replace', index=False)
    return {"message" : "success!"}
   except Exception as e:
      raise e

