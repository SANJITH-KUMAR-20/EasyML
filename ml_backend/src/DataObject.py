from typing import *
import pandas as pd
class DataObj:

    def __init__(self, data, name) -> None:

        """
        class is used to version a csv data in the form of a pandas dataframe

        Args:

        data -> pd.DataFrame: CSV data
        name -> str: name of the dataset
        
        """

        self.curr_state = data
        self.prev_states = [] #stores the previous states of the data (versioning part)
        self.name = name

    def change_state(self, new_state) -> None:

        """
        used to change the current state of the data object

        Args:

        new_state -> pd.DataFrame : New CSV data
        """
        self.prev_states.append(self.curr_state)
        self.curr_state = new_state

    def get_state(self) -> pd.DataFrame:
        """
        Returns the current state of the data

        Returns:
        curr_state -> pd.DataFrame : CSV data
        """
        return self.curr_state
    
    def return_prev_state(self) -> None:
        """
        changes the current state to the previous state
        """
        self.curr_state = self.prev_states.pop()

    def get_name(self) -> str:
        """
        Returns the name of the dataset

        Returns:
        name -> str : name of the dataset
        """
        return self.name