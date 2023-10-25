import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.CT_CD_pipeline import CT_CD_pipeline
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri

def set_env_variable():
    uri = str(get_tracking_uri())
    with open('temp_set_env.sh', 'w') as f:
        f.write(f"export MLFLOW_TRACKING_URI='{uri}'")
if __name__ == "__main__":
    set_env_variable()
   # CT_CD_pipeline() 