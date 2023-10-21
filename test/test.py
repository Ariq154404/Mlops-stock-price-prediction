import requests
import json
import pandas as pd

def get_forecast(interval):
    # Define the API endpoint
    url = "http://localhost:5001/forecast"

    # Create the data payload
    payload = {
        "interval": interval
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # If request was successful, return the returned data
    if response.status_code == 200:
        forecast_data = json.loads(response.text)
        if isinstance(forecast_data, str):
            forecast_data = json.loads(forecast_data)
        return forecast_data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def convert_to_dataframe(forecast_data):
    # Convert timestamps to datetime format
    for data_point in forecast_data:
        print(type(data_point))
        data_point["ds"] = pd.to_datetime(int(data_point["ds"]), unit='ms')
        
    # Convert the list to a DataFrame
    df = pd.DataFrame(forecast_data)

    return df

if __name__ == "__main__":
    interval = "5T"  # example interval, adjust as needed
    
    forecast = get_forecast(interval)
    print(forecast)
    if forecast:
        df = convert_to_dataframe(forecast)
        print(df.info())
        print(df)
