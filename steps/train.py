# train.py
import logging
from prophet import Prophet
from zenml.steps import step
import pandas as pd
from zenml import step
from zenml.client import Client
from typing_extensions import Annotated
experiment_tracker = Client().active_stack.experiment_tracker
#print(experiment_tracker.name)
class TrainModel:
    def __init__(self, train_ratio=0.8):
        self.train_ratio = train_ratio

    def train(self, df):
        df = df.rename(columns={'stock_date': 'ds', 'stock_price': 'y'})
        train_size = int(self.train_ratio * len(df))
        train_df = df[:train_size]
        test_df = df[train_size:]
        model = Prophet()
        model.add_seasonality(name='hourly', period=24/4, fourier_order=8)
        model.fit(train_df)
        future = model.make_future_dataframe(periods=len(test_df),freq='5T')
        forecast = model.predict(future)
        forecasted_values = forecast['yhat'][train_size:]
        return model, test_df,forecasted_values

@step(experiment_tracker="mlflow_tracker")
def train_model(df) -> (Annotated[Prophet, "prophet_model"], pd.DataFrame, pd.DataFrame):
    try:
        trainer = TrainModel()
        model, test_df, forecasted_values = trainer.train(df)
        return model, test_df, forecasted_values
    except Exception as e:
        logging.error(e)
        raise e
