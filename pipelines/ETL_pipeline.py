import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.producer import produce
from steps.consumer import consume
from zenml import pipeline

@pipeline(enable_cache=False)
def ETL_pipeline() -> None:
    consume.after(produce)
    status = produce()
    consume(status)
# if __name__ == "__main__":
#     ETL_pipeline() 
