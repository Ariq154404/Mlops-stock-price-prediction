import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.ETL_pipeline import ETL_pipeline
from zenml.config.schedule import Schedule

if __name__ == "__main__":
    schedule = Schedule(cron_expression="*/5 * * * *")
    epl=ETL_pipeline.with_options(schedule=schedule)
    epl()
    # ETL_pipeline()
    
    
    