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


app = FastAPI()

dataset = {}

@app.get("/get_columns")
async def get_columns():
   try:
        data = pd.read_csv("database/dummy_csv.csv")
        columns = ",".join(list(data.columns))
        return Response(content = columns, media_type="application/json")
   except Exception as e:
        return {"error":str(e)}
   