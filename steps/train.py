import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import mysql.connector
# import pickle
from joblib import dump

# Database configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PORT = 3307
MYSQL_PASSWORD = "my-secret-pw"
MYSQL_DATABASE = "stocks"

# Connect to MySQL and fetch stock data
def get_data():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    query = "SELECT * FROM stock_table ORDER BY stock_date"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def save(model):
    dump(model, 'prophet_model.joblib')
    # with open('prophet_model.pkl', 'wb') as f:
    #    pickle.dump(model, f)
def forecast_with_prophet(df):
    # Rename columns for Prophet compatibility
    df = df.rename(columns={'stock_date': 'ds', 'stock_price': 'y'})
    # df['ds'] = pd.to_datetime(df['ds']).dt.date
    print(df.info())
    # Splitting data into training and testing sets
    train_size = int(0.8 * len(df))
    train_df = df[:train_size]
    test_df = df[train_size:]
    print(train_df)
    # Creating and fitting the model
    model = Prophet()
    model.add_seasonality(name='hourly', period=24/4, fourier_order=8)
    model.fit(train_df)
    try:
        save(model)
    except Exception as e:
        print("model not saved")
    # Predicting on the test set
    future = model.make_future_dataframe(periods=len(test_df),freq='5T')
    forecast = model.predict(future)
    forecasted_values = forecast['yhat'][train_size:]
    print("test_df",test_df)
    print("fututure",forecast['ds'][train_size:])
    print("fututure",forecast['yhat'][train_size:])
    # print("forecasted_value",forecasted_values)
    return test_df['y'], forecasted_values
    

def evaluate_forecast(true_values, forecasted_values):
    mse = mean_squared_error(true_values, forecasted_values)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(true_values, forecasted_values)

    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Error (MAE): {mae}")

if __name__ == "__main__":
    # Fetch data
    df = get_data()

    # Forecast
    true_values, forecasted_values = forecast_with_prophet(df)

    # Evaluate the forecast
    evaluate_forecast(true_values, forecasted_values)
