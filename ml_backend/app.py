from fastapi import FastAPI, File, UploadFile, Response, Request
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
import dotenv

app = FastAPI()

content = dotenv.load_dotenv(".env")

#DOCKER MYSQL_SERVER VARIABLES
docker_host = os.getenv('DOCKER_DB_HOST', 'mysql_server')
docker_port = os.getenv('DOCKER_DB_PORT', '3306')
docker_user = os.getenv('DOCKER_DB_USER', 'root')
docker_password = os.getenv('MYSQL_ROOT_PASSWORD', 'rootpassword')
docker_database = os.getenv('MYSQL_DATABASE', 'mynewdatabase')
docker_password = quote_plus(docker_password)
#ENV VARIABLES
host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
database = os.environ['DATABASE']
password = quote_plus(password)

#CONNECTIONS
DATABASE_URL = f"mysql+pymysql://{user}:{password}@host.docker.internal/{database}"
DOCKER_DATABASE_URL = f"mysql+pymysql://{docker_user}:{docker_password}@{docker_host}:{docker_port}/{docker_database}"
redis_host = int(os.getenv('REDIS_HOST',6379))
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis = aioredis.from_url(f"redis://redis:{redis_port}", decode_responses=False)
session_id = str(uuid.uuid4())
engine = create_engine(DATABASE_URL)
docker_engine = create_engine(DOCKER_DATABASE_URL)


#ROUTES FOR LOGIN AND SESSION SETUP

@app.post("/create_account")
def create_or_login_account(login : LoginRequest):
    try:
        with engine.connect() as connection:
            if login.kind == "create_account":
                
                    result = connection.execute(text(f"SELECT EXISTS (SELECT 1 FROM user WHERE mail_id = '{login.email_id}') AS is_present"))
                    if result.fetchone()[0]:
                        return {"User account already exists"}
                    else:
                        if login.password != login.reconfirm_password:
                            return {"Enter the same password in both the fields"}
                        query = text(f"INSERT INTO user (user_name, mail_id, password) VALUES (:user_name, :email_id, :password)")
                        connection.execute(query, {"user_name": login.user_name, "email_id": login.email_id, "password": login.password})
                        connection.commit()
                        return {'msg' : "User Account Created Successfully."}
                        
            elif login.kind == "login":
                with engine.connect() as connection, docker_engine.connect() as docker_connection:
                    result = connection.execute(text(f"SELECT EXISTS (SELECT 1 FROM user WHERE mail_id = '{login.email_id}') AS is_present"))
                    if not result.fetchone()[0]:
                        return {"No such User account."}
                    else:
                        query = f"SELECT password,permanent_session_id FROM user WHERE mail_id = '{login.email_id}'"
                        result = connection.execute(text(query))
                        result = result.fetchone()
                        login_password = result[0]
                        if login_password == login.password:
                            session_id = result[1]
                            query = f"INSERT INTO usersession (user_session_id, model_table_name) VALUES ('{session_id.replace('-', '')}','{'model_'+session_id.replace('-', '')}')"
                            docker_connection.execute(text(query))
                            docker_connection.commit()
                            model_table_query = f"""
                                CREATE TABLE IF NOT EXISTS `{'model_'+session_id.replace('-', '')}` (
                                `model_id` VARCHAR (255) NOT NULL UNIQUE,
                                `model_name` VARCHAR(255),
                                `kind` VARCHAR(255),
                                `total_score` FLOAT,
                                `mse` FLOAT,
                                `mae` FLOAT,
                                `r2` FLOAT,
                                `accuracy` FLOAT,
                                `precision` FLOAT,
                                `recall` FLOAT,
                                `f1` FLOAT,
                                `ari` FLOAT,
                                `nmi` FLOAT,
                                `sil` FLOAT,
                                PRIMARY KEY(`model_id`)
                                );"""
                            docker_connection.execute(text(model_table_query))
                            docker_connection.commit()
                        
                            return {'msg' : 'successful login', 'status' : True, 'sessionid' : session_id}
    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate_model")
async def evaluate_model(request : EvaluateModelRequest):

    try:
        with docker_engine.connect() as docker_connection:
            s_id = request.user_session_id.replace('-', '')
            query = f"SELECT model_table_name FROM usersession WHERE user_session_id = '{s_id}'"
            result = docker_connection.execute(text(query))
            model_table_name = result.fetchone()[0]
            for model_name, kind in zip(request.model_name, request.model_kind):
                query = f"SELECT model_id FROM {model_table_name} WHERE model_name = '{model_name}'"
                result = docker_connection.execute(text(query))
                model_id = result.fetchone()[0]
                pickled_file = await redis.get(model_id)
                model = pickle.loads(pickled_file)
                if request.evaluation_on == "test_set":
                    test_x,test_y = get_data(docker_engine,request.dataset,type="test")
                else:
                    test_x,test_y = get_data(docker_engine, request.dataset,type="test_data")
                results = evaluate(kind,model,(test_x,test_y))
                if kind == "regression":
                    mse, mae, r2 = round(results["mse"],3), round(results["mae"],3), round(results["r2"],3)
                    query =f"UPDATE {model_table_name} SET mse = '{mse}', mae = '{mae}', r2 = '{r2}', kind = 'Regression', WHERE model_id = '{model_id}'"
                    docker_connection.execute(text(query))
                    docker_connection.commit()
                    query = f"UPDATE {model_table_name} SET total_score = (COALESCE(mse,0) + COALESCE(mae,0) + COALESCE(r2,0))/3"
                    
                elif kind == "classification":
                    acc, pre, recall,f1 = round(results["accuracy"],3), round(results["prec"],3), round(results["recall"],3), round(results["f1"],3)
                    query  = f"UPDATE {model_table_name} SET accuracy = '{acc}', `precision` = '{pre}', recall = '{recall}',kind = 'Classification', f1 = '{f1}' WHERE model_id = '{model_id}'"
                    docker_connection.execute(text(query))
                    docker_connection.commit()
                else:
                    raise HTTPException(status_code=500, detail=f"No such kind")
                docker_connection.execute(text(query))
                docker_connection.commit()


    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/model-results")
def results_model_table(request : TableRequest):
    try:
        with docker_engine.connect() as doc_connection, engine.connect() as connection:
            if request.table_kind != "user_table":
                result = doc_connection.execute(text(f"SELECT * FROM {request.table_name}"))
            rows = result.fetchall()
            column_names = result.keys()

        df = pd.DataFrame(rows, columns=column_names)
        csv_data = df.to_csv(index=False)
        
        return Response(content=csv_data, media_type="text/csv")

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            
            data.to_sql(name, con=docker_engine, if_exists='replace', index=False)
            # if not os.path.exists("../temp"):
            #     os.mkdir("../temp")
            
            return {"message": "success!"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    
@app.get("/show-table/{table_name}")
async def view_table_as_csv(table_name: str):
    try:
        with docker_engine.connect() as connection:
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
        with docker_engine.connect() as connection:
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

        with docker_engine.connect() as connection:
            connection.execute(text(query))

        return {"message": "Column dropped successfully"}

    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/manipulate/{kind}")
def manipulate(config: ManipulateRequest, kind:str):
     try:
        with docker_engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.table_name}"))
            rows = result.fetchall()
            column_names = result.keys()
        if kind == "encode_data":
            df = pd.DataFrame(rows, columns=column_names)
            data = encode(config, df)
            data.to_sql(config.table_name, con=docker_engine, if_exists='replace', index=False)
            return {"message": "Encoding successful"}
        elif kind == "standardize_data":
            df = pd.DataFrame(rows, columns=column_names)
            data = standardize(config, df)
            data.to_sql(config.table_name, con=docker_engine, if_exists='replace', index=False)
            return {"message": "Standard Encoding successful"}
        elif kind == "impute_data":
            df = pd.DataFrame(rows, columns=column_names)
            data = impute_columns(config, df)
            data.to_sql(config.table_name, con=docker_engine, if_exists='replace', index=False)
            return {"message": "Impute successful"}
        else:
            raise HTTPException(status_code=500, detail = f"no such manipulation strategy : {kind}")

     except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
     except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/split-data")
async def split_data(config : SplittingRequest):
    try:
        with docker_engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {config.dataset_name}"))
            rows = result.fetchall()
            column_names = result.keys()
        df = pd.DataFrame(rows, columns=column_names)
        x_train,y_train,x_test,y_test = split(config,df)
        names = save_splits(docker_engine,config.dataset_name,(x_train,y_train,x_test,y_test))
        return {"successful split"}
    except SQLAlchemyError as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=f"split_data_{str(e)}")    
    
@app.post("/train-model")
async def train_model(config :TrainRequest):
    try:

        mod = train(config, docker_engine)
        with docker_engine.connect() as docker_connection:
            s_id = config.user_session_id.replace('-', '')
            query = f"SELECT model_table_name FROM usersession WHERE user_session_id = '{s_id}'"
            result = docker_connection.execute(text(query))
            model_table_name = result.fetchone()[0]
            model_id = config.user_session_id.replace('-', '') + config.model_name
            query= f"INSERT INTO {model_table_name} (model_id, model_name, kind) VALUES ('{model_id}', '{config.model_name}','{config.type}')"
            docker_connection.execute(text(query))
            docker_connection.commit()
            pickled_model = pickle.dumps(mod)
            await redis.set(model_id, pickled_model)

        return {"successfully trained the model"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.get("/download-model")
async def download_model(config : DownloadRequest):
    try:
        with docker_engine.connect() as docker_connection:
            s_id = config.user_session_id.replace('-', '')
            query = f"SELECT model_table_name FROM usersession WHERE user_session_id = '{s_id}'"
            result = docker_connection.execute(text(query))
            model_table_name = result.fetchone()[0]
            if config.is_best:
                sort_evaluation_scores(docker_engine,model_table_name,config.kind)
                results = get_best(docker_engine,model_table_name,config.kind)
                model_id = results[config.kind][model_id]
            else:
                model_id = config.user_session_id.replace('-', '') + config.model_name
        
        
        pickled_file = await redis.get(model_id)
        # model = pickle.loads(pickled_file)
        file_like = io.BytesIO(pickled_file)
        file_like.seek(0)

        return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={session_id}_model.pkl"}
        )
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
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