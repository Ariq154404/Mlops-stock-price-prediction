import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.ingest import ingest_data
from steps.EDA import EDA
from typing import Tuple
from zenml import step
from zenml import pipeline

@pipeline(enable_cache=False)
def EDA_pipeline() -> None:
    df=ingest_data("localhost", "root", 3307, "my-secret-pw", "stocks")
    EDA(df,'stock_date','stock_price')
# if __name__ == "__main__":
#     EDA_pipeline() 