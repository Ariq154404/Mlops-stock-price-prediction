import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.EDA_pipeline import EDA_pipeline
from zenml.config.schedule import Schedule
if __name__ == "__main__":
    schedule = Schedule(cron_expression="*/5 * * * *")
    eda=EDA_pipeline.with_options(schedule=schedule)
    eda()
    #EDA_pipeline() 