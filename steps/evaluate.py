import logging

from src.evaluation import MSE, MAE, R2
from zenml import step 
import pickle
from typing import Tuple
from typing_extensions import Annotated
from sklearn.base import RegressorMixin
import pandas as pd

@step
def evaluate_model(model:RegressorMixin,
                   x_test: pd.DataFrame,
                    y_test: pd.DataFrame )->Tuple[
                        Annotated[float, "r2"],
                        Annotated[float, "mse"],
                    ]:

    """
    Evaluates a model on the given data:
    -------------------------------------
    Args: 
        model:RegressorMixin(Input_model),
        x_test: pd.DataFrame(test data),
        y_test: pd.DataFrame(true labels)

    Returns:
        r2_score: float
        mse: float
    
    """
    prediction = model.predict(x_test)
    mse_class = MSE()
    mse = mse_class.calculate_scores(y_test.to_numpy, prediction)

    r2_score = R2()
    r2 = r2_score.calculate_scores(y_test.to_numpy, prediction)

    return r2, mse