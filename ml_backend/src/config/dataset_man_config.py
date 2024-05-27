#CONFIG FOR DATASET MANIPULATION TASK
from typing import *
from pydantic import BaseModel,Field


class Specific:

    kind : str



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

class ImputeRequest(BaseModel):
    """
    Config for imputation
    """
    strategy: str = Field("Simple Imputer", description="Imputation strategy (e.g., 'Simple Imputer', 'KNN Imputer')")
    columns: List[str] = Field(..., description="List of columns to impute")
    table_name: str = Field(..., description="Name of the table")
    parameters: Dict[str, Union[int, str, float]] = Field(default_factory=dict, description="Parameters for the imputation strategy")

    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "Simple Imputer",
                "columns": ["column1", "column2"],
                "table_name": "your_table",
                "parameters": {"strategy": "mean"}
            }
        }
