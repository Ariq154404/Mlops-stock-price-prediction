import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.EDA_pipeline import EDA_pipeline

if __name__ == "__main__":
    EDA_pipeline() 