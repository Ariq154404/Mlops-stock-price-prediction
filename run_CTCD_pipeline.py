import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.CT_CD_pipeline import CT_CD_pipeline

if __name__ == "__main__":
    CT_CD_pipeline() 