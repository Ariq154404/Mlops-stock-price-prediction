import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.ETL_pipeline import ETL_pipeline
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri


if __name__ == "__main__":
    os.environ["MLFLOW_TRACKING_URI"] = get_tracking_uri()
    ETL_pipeline() 