# ingest.py
import logging
import pandas as pd
import mysql.connector
from zenml import step

class IngestData:
    """
    Data ingestion class which ingests data from the source and returns a DataFrame.
    """

    def __init__(self, host, user, port, password, database) -> None:
        """Initialize the data ingestion class."""
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

    def get_data(self) -> pd.DataFrame:
        conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        query = "SELECT * FROM stock_table ORDER BY stock_date"
        df = pd.read_sql(query, conn)
        conn.close()
        return df

@step
def ingest_data(host, user, port, password, database) -> pd.DataFrame:
    try:
        ingest_data = IngestData(host, user, port, password, database)
        df = ingest_data.get_data()
        return df
    except Exception as e:
        logging.error(e)
        raise e
