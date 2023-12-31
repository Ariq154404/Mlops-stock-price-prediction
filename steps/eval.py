# evaluation.py
import logging
import pandas  as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from zenml import step
import mlflow
class EvaluateModel:
    def __init__(self):
        pass

    def evaluate(self, true_values, forecasted_values):
        mse = mean_squared_error(true_values, forecasted_values)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(true_values, forecasted_values)
        return mse, rmse, mae


@step(experiment_tracker="mlflow")
def evaluate_model(true_values : pd.DataFrame, forecasted_values : pd.Series) -> dict:
    try:
        evaluator = EvaluateModel()
        mse, rmse, mae = evaluator.evaluate(true_values, forecasted_values)
        mlflow.log_metric("mae", mse)
        return {"mse": mse, "rmse": rmse, "mae": mae}
    except Exception as e:
        logging.error(e)
        raise e
