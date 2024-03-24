from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import os
import pandas as pd
import sqlite3

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
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

