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
from zenml.integrations.mlflow.steps.mlflow_registry import mlflow_register_model_step
from zenml.integrations.mlflow.steps.mlflow_deployer import( 
    mlflow_model_registry_deployer_step,
    mlflow_model_deployer_step
)
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.client import Client
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step
from mlflow.tracking import MlflowClient
import mlflow
import subprocess
# os.environ["MLFLOW_TRACKING_URI"] = get_tracking_uri()

@step
def deployer(model_name : str, status: bool) -> None:
    if not status:
        return 
    most_recent_model_version_number = Client() .active_stack.model_registry.list_model_versions(metadata={})[0].version
    model_deployer = mlflow_model_registry_deployer_step(
        registry_model_name=model_name,
        registry_model_version=most_recent_model_version_number,
        timeout = 300
           )
    # print("TYPE",type(model_deployer))

@step
def deployment_trigger(
    result: dict,

) -> bool:
    """Implements model deployment trigger"""

    return result["mae"] < 100
# @step
# def serve_mlflow_model(model_name: str, model_version: str) -> None:
#     """Serve an MLflow registered model using the specified name and version."""
#     tracking_uri=Client().active_stack.experiment_tracker.get_tracking_uri()
#     #print(tracking_uri,type(tracking_uri))
#     mlflow.set_tracking_uri(tracking_uri)
#     clnt = MlflowClient()
#     for rm in clnt.search_registered_models():
#         print(rm.name)
#     cmd = [
#         "mlflow", "models", "serve",
#         "-m", f"models:/{model_name}/{model_version}",
#         "-p", "1234",  # specify the port number here
#         "--no-conda"
#     ]
#     env = os.environ.copy()
#     env["MLFLOW_TRACKING_URI"] = tracking_uri
    
#     subprocess.run(cmd,env=env)
    
    
@pipeline(enable_cache=False)
def CT_CD_pipeline() -> None:
    df=ingest_data("localhost", "root", 3307, "my-secret-pw", "stocks")
    print(df)
    model, test_df, forecasted_values = train_model(df)
    result=evaluate_model(test_df, forecasted_values)
    model_name = "zenml-prophet-model5"
    register_model = mlflow_register_model_step.with_options(
    parameters=dict(
        name=model_name,
        description="This is the first test of the project run",
    )
      )
    register_model(model,trained_model_name="prophet_model5")
    status = deployment_trigger(result)
    if status:
        deployer(model_name,status)
        # version=Client().active_stack.model_registry.list_model_versions(metadata={})[0].version
        # deployment_service=mlflow_model_registry_deployer_step(
        # registry_model_name=model_name,
        # registry_model_version=version )
    #mlflow_model_deployer_step(model=model,deploy_decision=deployment_trigger(result),model_name="zenml-prophet-model")
    
    #print("result",result)
    # if deployment_trigger(result):
    #     version=Client().active_stack.model_registry.list_model_versions(metadata={})[0].version
    #     serve_mlflow_model(model_name,version)
        
        
# if __name__ == "__main__":
#     CT_CD_pipeline() 
    