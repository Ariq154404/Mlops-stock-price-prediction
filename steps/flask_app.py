from flask import Flask, request, jsonify
import pandas as pd
from prophet import Prophet
from joblib import load

app = Flask(__name__)

# Load the trained model
model = load('prophet_model.joblib')

@app.route('/forecast', methods=['POST'])
def forecast():
    interval = request.json.get('interval')  # format: "5min", "1h", etc.
    
    future = model.make_future_dataframe(periods=10, freq=interval)
    forecast = model.predict(future)
    forecast_json = forecast[['ds', 'yhat']].tail(10).to_json(orient='records')
    # Convert forecast dataframe to json
    # forecast_json = forecast[['ds', 'yhat']].to_json(orient='records')

    return jsonify(forecast_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
