from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse, FileResponse
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
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.utils.sql import save_splits
import yaml
from redis import asyncio as aioredis
import pickle
import io
import uuid
import uvicorn

app = FastAPI()


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
DATABASE_URL = f"mysql+pymysql://{user}:{password}@host.docker.internal/{database}"
redis = aioredis.from_url("redis://localhost", decode_responses=False)

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
            if not os.path.exists("../temp"):
                os.mkdir("../temp")
            
            return {"message": "success!"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    
@app.get("/download-table/{table_name}")
async def download_table_as_csv(table_name: str):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            column_names = result.keys()

        df = pd.DataFrame(rows, columns=column_names)
        csv_data = df.to_csv(index=False)
        
        return Response(content=csv_data, media_type="text/csv")

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-data/{table_name}")
async def delete_table(table_name: str):
    try:
        with engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        
        return {"message": "Data deleted successfully"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/drop-column")
async def drop_column(para: DropColumnsRequest):
    try:
        drop_cols = ", ".join(f"DROP COLUMN {col}" for col in para.columns)
        query = f"ALTER TABLE {para.table_name} {drop_cols}"

        with engine.connect() as connection:
            connection.execute(text(query))

        return {"message": "Column dropped successfully"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/impute-data")
async def impute_data(config: ImputeRequest):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.table_name}"))
            rows = result.fetchall()
            column_names = result.keys()

        df = pd.DataFrame(rows, columns=column_names)
        data = impute_columns(config, df)
        data.to_sql(config.table_name, con=engine, if_exists='replace', index=False)

        return {"message": "Imputation successful"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/standardize-data")
async def standardize_data(config: StandardizeRequest):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.table_name}"))
            rows = result.fetchall()
            column_names = result.keys()

        df = pd.DataFrame(rows, columns=column_names)
        data = standardize(config, df)
        data.to_sql(config.table_name, con=engine, if_exists='replace', index=False)

        return {"message": "Scaling successful"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/encode-data")
async def encode_data(config: StandardizeRequest):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.table_name}"))
            rows = result.fetchall()
            column_names = result.keys()

        df = pd.DataFrame(rows, columns=column_names)
        data = encode(config, df)
        data.to_sql(config.table_name, con=engine, if_exists='replace', index=False)

        return {"message": "Encoding successful"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/split-data")
def split_data(config : SplittingRequest):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.dataset_name}"))
            rows = result.fetchall()
            column_names = result.keys()
        df = pd.DataFrame(rows, columns=column_names)
        x_train,y_train = split(config,df)
        names = save_splits(engine,config.dataset_name,(x_train,y_train))
        config = {
        "train_x" : names[0],
        "train_y" : names[1],
        "session_id" : str(uuid.uuid4())
        }
        with open('../temp/session_config.yaml', 'w') as file:
            yaml.dump(config, file)
        return {"successful split"}
    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=str(e))    
    
@app.post("/train-model")
async def train_model(config :TrainRequest):
    try:
        
        mod = train(config, engine)

        with open('../temp/session_config.yaml', 'r') as file:
            session_config = yaml.safe_load(file)
        session_id = session_config["session_id"]
        pickled_model = pickle.dumps(mod)
        await redis.set(session_id, pickled_model)

        return {"successfully trained the model"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.get("/download-model")
async def download_model(response: Response):
    try:
        with open('../temp/session_config.yaml', 'r') as file:
            session_config = yaml.safe_load(file)
        session_id = session_config["session_id"]
        pickled_file = await redis.get(session_id)
        # model = pickle.loads(pickled_file)
        file_like = io.BytesIO(pickled_file)
        file_like.seek(0)

        return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={session_id}_model.pkl"}
        )
    except Exception as e:
        raise e
    
@app.delete("/end-session")
async def delete_session():
    try:
        with open('../temp/session_config.yaml', 'r') as file:
                session_config = yaml.safe_load(file)
        session_id = session_config["session_id"]
        result = await redis.delete(session_id)
        assert result == 1
        if os.path.exists("../temp"):
            os.removedirs("../temp")
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)