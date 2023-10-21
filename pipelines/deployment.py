import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.ingest import ingest_data
from steps.train import train_model
from steps.eval import evaluate_model
from typing import Tuple
from zenml import step
from zenml import pipeline
from zenml.integrations.mlflow.steps.mlflow_registry import (
    mlflow_register_model_step,
)
from zenml.integrations.mlflow.steps.mlflow_deployer import (
    mlflow_model_registry_deployer_step,
)
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.client import Client


# os.environ["MLFLOW_TRACKING_URI"] = get_tracking_uri()



@step
def deployment_trigger(
    mae: float,

) -> bool:
    """Implements model deployment trigger"""

    return mae < 100
# @step
# def deployment(model_name) -> None:
#     most_recent_model_version_number = int(
#     Client()
#     .active_stack.model_registry.list_model_versions(metadata={})[0]
#     .version
#     )
#     model_deployer = mlflow_model_registry_deployer_step.with_options(
#     parameters=dict(
#         registry_model_name=model_name,
#         registry_model_version=most_recent_model_version_number,
#     )
#     )
    
@pipeline(enable_cache=True)
def CT_CD_pipeline() -> None:
    df=ingest_data("localhost", "root", 3307, "my-secret-pw", "stocks")
    model, test_df, forecasted_values = train_model(df)
    result=evaluate_model(test_df, forecasted_values)
    model_name = "zenml-prophet-model"
    register_model = mlflow_register_model_step.with_options(
    parameters=dict(
        name=model_name,
        description="This is the first test of the project run",
    )
      )
    register_model(model)
    if deployment_trigger(result["mse"]):
        most_recent_model_version_number = int(
           Client() .active_stack.model_registry.list_model_versions(metadata={})[0].version)
        model_deployer = mlflow_model_registry_deployer_step.with_options(
              parameters=dict(
        registry_model_name=model_name,
        registry_model_version=most_recent_model_version_number,
           )
           )
    
    
    
    