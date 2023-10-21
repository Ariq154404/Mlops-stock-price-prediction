import os
import sys
from prophet import Prophet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
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
def predictor(service: BaseService, interval: str) -> Annotated[pd.DataFrame, "output_dataframe"]:
    df=service.predict(interval)
    return df
    
@pipeline
def deploy_and_predict() -> pd.DataFrame:
    service=prediction_service_loader()
    df=service.predict("5T")
    return df
    