import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.ETL_pipeline import ETL_pipeline


if __name__ == "__main__":
    ETL_pipeline() 