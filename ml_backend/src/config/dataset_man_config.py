#CONFIG FOR DATASET MANIPULATION TASK
from typing import *
from pydantic import BaseModel,Field



class LoginRequest(BaseModel):
    """
    Config for Creating an Account
    """
    kind : str = Field("create_account", description="type of process, create account or login")
    user_name : str = Field("chevalier", description="the name of the user")
    email_id : str = Field("hfghfghd@gmail.com", description= "the mail id of the user")
    password: str
    reconfirm_password : str = None


class DataConfig(BaseModel):

    """
    Config format for manipulating data
    """

    dataset_name : str = "dummy"
    task : Literal['Drop', 'Scale', 'Standardize', 'Apply']
    columns : List[str]

class DropColumnsRequest(BaseModel):

    """
    Config for dropping column
    """

    table_name: str
    columns: list[str]

class ManipulateRequest(BaseModel):

    kind: str = Field("encode_data", description= "manipulation type i.e. 'encode_data','standardize_data','impute_data'")
    strategy: str = Field("Simple_Imputer", description="Imputation strategy (e.g., 'Simple Imputer', 'KNN Imputer')")
    columns: List[str] = Field(..., description="List of columns to impute")
    table_name: str = Field(..., description="Name of the table")
    parameters: Dict[str, Union[int, str, float]] = Field(default_factory=dict, description="Parameters for the imputation strategy")

    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "Simple_Imputer",
                "columns": ["column1", "column2"],
                "table_name": "your_table",
                "parameters": {"strategy": "mean"}
            }
        }




class ImputeRequest(BaseModel):
    """
    Config for imputation
    """
    strategy: str = Field("Simple_Imputer", description="Imputation strategy (e.g., 'Simple Imputer', 'KNN Imputer')")
    columns: List[str] = Field(..., description="List of columns to impute")
    table_name: str = Field(..., description="Name of the table")
    parameters: Dict[str, Union[int, str, float]] = Field(default_factory=dict, description="Parameters for the imputation strategy")

    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "Simple_Imputer",
                "columns": ["column1", "column2"],
                "table_name": "your_table",
                "parameters": {"strategy": "mean"}
            }
        }


class StandardizeRequest(BaseModel):

    """
    Config for standardization
    """

    strategy : str = Field("MinMaxScalar", description= "Standardization strategy (e.g., 'MinMax Scalar', 'Standard Scalar')")
    columns: List[str] = Field(..., description="List of columns to impute")
    table_name: str = Field(..., description="Name of the table")
    parameters: Dict[str, Union[int, str, float]] = Field(default_factory=dict, description="Parameters for the standarization strategy")

    class Config:
        json_schema_extra = {
            "example" : {
                "strategy": "MinMax Scaler",
                "columns": ["column1", "column2"],
                "table_name": "your_table",
                "parameters": {"feature_range": (5,5)}
            }
        }

class EncodeRequest(BaseModel):

    """
    Config for encoding
    """

    strategy : str = Field("OneHotEncoder", description= "Encoding strategy (e.g., 'OrdinalEncoder', 'OneHotEncoder', 'LabelEncoder')")
    columns: List[str] = Field(..., description="List of columns to encode")
    table_name: str = Field(..., description="Name of the table")
    parameters: Dict[str, Union[int, str, float]] = Field(default_factory=dict, description="Parameters for the encoding strategy")

    class Config:
        json_schema_extra = {
            "example" : {
                "strategy": "OneHotEncoder",
                "columns": ["column1", "column2"],
                "table_name": "your_table",
                "parameters": {}
            }
        }

class TrainRequest(BaseModel):

    """
    Config for Training a model.
    """

    type : str = Field("Regression", description="Type of problem i.e. Classification , Regression...")
    strategy : str = Field("LinearRegression", description= "Type of model to train i.e. Linear Regressor,Logistic Regressor")
    dataset_name : str = Field(..., description="Name of the table or dataset")
    parameters : Dict[str, Union[int,str,float]] = Field(default_factory=dict, description="parameter for training the model.")

    class Config:
        json_schema_extra = {
            "example" : {
                "type" : "Regression",
                "strategy" : "Linear Regression",
                "dataset_name" : "your_dataset_name",
                "parameters" : {}
            }
        }
 

class SplittingRequest(BaseModel):

    """
    Config for splitting data
    """
    train_test_split : float = Field(...,description="train test split percentage")
    dataset_name : str = Field(..., description="Name of the table or dataset to split")
    strategy : str = Field(..., description= "strategy to split")
    parameters : Dict[str, Union[int,str,float]] = Field(default_factory=dict, description="parameter for splitting data.")
    y_column : str = Field(..., description= "Column to Predict")
    
    class Config:
        json_schema_extra = {
            "example": {
                "train_test_split" : "0.8",
                "dataset_name" : "your_table_name",
                "strategy" : "TrainTestSplit",
                "parameters" : {
                    "shuffle" : True
                },
                "y_column" : "column_to_predict"
            }
        }
