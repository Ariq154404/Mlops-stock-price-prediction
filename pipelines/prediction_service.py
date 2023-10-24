import os
import sys
from prophet import Prophet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from zenml import step
from zenml import pipeline
from zenml.integrations.mlflow.steps.mlflow_registry import (
    mlflow_register_model_step,
)
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.client import Client
from zenml.services import BaseService
from typing_extensions import Annotated

@step(enable_cache=False)
def prediction_service_loader() -> BaseService:
    """Load the model service of our train_and_register_model_pipeline."""
    client = Client()
    model_deployer = client.active_stack.model_deployer
    services = model_deployer.find_model_server(
        pipeline_name="CT_CD_pipeline",
        running=True,
    )
    return services[0]
@step
def predictor(service: BaseService, model_input: dict) -> Annotated[pd.DataFrame, "output_dataframe"]:
    # future = service.make_future_dataframe(periods=model_input["len"], freq=model_input["freq"])
#     test=  {
#     'ds': ['2023-10-17 00:00:00', '2023-10-17 00:15:00'],
#     'yhat': [1.23, 2.34]  # Sample float values
#    }
#     future = pd.DataFrame(test)
    #future['ds'] = pd.to_datetime(future['ds'])
    #json_string = future.to_json(date_format='iso', orient='records')
    #df = pd.DataFrame(model_input,index=[0])
    forecast = service.predict(np.array([model_input]))
    return forecast[['ds', 'yhat']].tail(10)
    
    
@pipeline
def deploy_and_predict() -> BaseService:

    service=prediction_service_loader()
    print(type(ser))
    #df = predictor(service,{'period': 10, 'freq': '5T'})
    return service
if __name__ == "__main__":
    df=deploy_and_predict() 
    print("TYYYPE",df)
    