#CONFIG FOR DATASET MANIPULATION TASK
from typing import *
from pydantic import BaseModel


class Specific:

    kind : str



class DataConfig(BaseModel):

    """
    Config format for manipulating data
    """

    dataset_name : str = "dummy"
    task : Literal['Drop', 'Scale', 'Standardize', 'Apply']
    columns : List[str]
