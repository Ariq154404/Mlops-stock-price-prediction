import requests
import pandas as pd
from datetime import datetime, timedelta
from zenml.integrations.mlflow.steps.mlflow_registry import mlflow_register_model_step
from zenml.client import Client
from zenml.services import BaseService
class ProphetPredictor:

    def __init__(self, endpoint_url=None):
        client = Client()
        model_deployer = client.active_stack.model_deployer
        services = model_deployer.find_model_server(
        pipeline_name="CT_CD_pipeline",
        running=True,
        )
        self.endpoint_url =  str(services[0].endpoint.prediction_url)
      

    @staticmethod
    def freq_to_timedelta(freq: str) -> timedelta:
        """Convert freq string to timedelta."""
        if freq.endswith("T"):
            minutes = int(freq[:-1])
            return timedelta(minutes=minutes)
        elif freq.endswith("D"):
            days = int(freq[:-1])
            return timedelta(days=days)
        # Add additional cases if needed
        raise ValueError(f"Unsupported freq value: {freq}")

    def send_prediction(self, future_params: dict) -> pd.DataFrame:
        """Send a prediction request to the served model using the given future parameters."""
        
        # Generate future dataframe based on the provided parameters
        periods = future_params["periods"]
        freq = future_params["freq"]
        delay = self.freq_to_timedelta(freq)
        
        last_date = datetime.now()  - timedelta(days=1) # or any starting point you desire
        future_dates = [(last_date + i * delay).strftime('%Y-%m-%d %H:%M:%S') for i in range(periods)]
        future_df = pd.DataFrame({'ds': future_dates})
        
        # Convert the dataframe to the expected JSON format
        request_data = {"dataframe_records": future_df.to_dict(orient='records')}
        
        response = requests.post(
            self.endpoint_url,
            headers={"Content-Type": "application/json"},
            json=request_data
        )
        
        # Check the response and convert to dataframe
        if response.status_code == 200:
            result = response.json()["predictions"]
            if isinstance(result, list) and all(isinstance(item, dict) for item in result):
                nr = pd.DataFrame(result)
                nr['ds'] = pd.to_datetime(nr['ds'])
                return nr[["ds", "yhat"]]
            else:
                raise ValueError(f"Unexpected response format")
        else:
            raise Exception(f"Request failed with status {response.status_code}. {response.text}")


# Example usage
# if __name__ == "__main__":
#     predictor = ProphetPredictor()
#     future_params = {'periods': 5, 'freq': '15T'}
#     predictions_df = predictor.send_prediction(future_params)
#     print(predictions_df)
# from zenml.client import Client
# from zenml.services import BaseService
# client = Client()
# model_deployer = client.active_stack.model_deployer
# services = model_deployer.find_model_server(
#         pipeline_name="CT_CD_pipeline",
#         running=True,
#     )
# print(services[0].endpoint.prediction_url)