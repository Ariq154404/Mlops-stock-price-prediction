# train.py
import logging
from prophet import Prophet
from zenml.steps import step
import pandas as pd
from zenml import step
from zenml.client import Client
from typing_extensions import Annotated
import mlflow
experiment_tracker = Client().active_stack.experiment_tracker
from typing import Tuple
#print(experiment_tracker.name)
# class ProphetWrapper(Prophet):

#     # def load_context(self, context):
#     #     self.model = Prophet()  # Initialize Prophet model
        
#     def predict(self, context, model_input):
#         future = self.model.make_future_dataframe(periods=model_input["len"],freq=model_input["freq"])
#         return self.model.predict(future)
# class ExtendedProphet(Prophet):

#     def predict(self, future_params=None):
#         """
#         Overridden predict method to create a future dataframe based on
#         provided period and frequency.
        
#         Parameters:
#         - df: pandas DataFrame with 'ds' column for dates (same as original Prophet)
#         - future_params: dictionary with keys 'period' and 'freq' specifying
#                          how to generate the future dataframe

#         Returns:
#         - forecast: a pandas DataFrame with the forecast
#         """
#         # Extract period and freq from future_params
#         period = future_params.get('period')
#         freq = future_params.get('freq')
        
#         if period is None or freq is None:
#             raise ValueError("`period` and `freq` must be provided in `future_params`")
        
#         # Create a future dataframe based on period and freq
#         future_df = self.make_future_dataframe(periods=period, freq=freq)
        
#         # Use the original Prophet predict method with the generated future dataframe
#         return super().predict(future_df)
class TrainModel:
    def __init__(self, train_ratio=0.8):
        self.train_ratio = train_ratio
        
    def train(self, df):
        df = df.rename(columns={'stock_date': 'ds', 'stock_price': 'y'})
        # Ensure the dataframe has regular intervals
    #     df.set_index('ds', inplace=True)
    #     all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='5min')
    #     df = df.reindex(all_dates)
    #     df.index.name = 'ds'
    
    # # Fill missing values with average of neighbors
    #     df['y'] = (df['y'].ffill() + df['y'].bfill()) / 2
    #     df['y'].fillna(method='ffill', inplace=True)
    #     df['y'].fillna(method='bfill', inplace=True)
    #     df.reset_index(inplace=True)
        train_size = int(self.train_ratio * len(df))
        train_df = df[:train_size]
        test_df = df[train_size:]
        model = Prophet()
        model.add_seasonality(name='hourly', period=24/4, fourier_order=8)
        model.fit(train_df)
        future = model.make_future_dataframe(periods=len(test_df),freq='5T')
        forecast = model.predict(future)
        forecasted_values = forecast['yhat'][train_size:]
        return model, test_df['y'],forecasted_values

@step(experiment_tracker="mlflow")
def train_model(df : pd.DataFrame) -> Tuple[Annotated[Prophet, "prophet_model"], pd.Series, pd.Series]:
    try:
        trainer = TrainModel()
        model, test_df, forecasted_values = trainer.train(df)
        mlflow.prophet.log_model(model, artifact_path="prophet_model5")
        #mlflow.pyfunc.log_model("prophet_model", python_model=model)
        return model, test_df, forecasted_values
    except Exception as e:
        logging.error(e)
        raise e
