import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector
import time
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.prediction import ProphetPredictor
# Streamlit configuration
st.set_page_config(
    page_title="Live Stock Prices Dashboard",
    page_icon="📈",
    layout="wide",
)

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
    query =  query = """
    SELECT * FROM stock_table 
    WHERE stock_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    ORDER BY stock_date DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def get_forecast(interval,freq):
    predictor = ProphetPredictor()
    future_params = {'periods': interval, 'freq': freq}
    predictions_df = predictor.send_prediction(future_params)
    return predictions_df
    # url = "http://localhost:5001/forecast"
    # payload = {
    #     "interval": interval
    # }
    # response = requests.post(url, json=payload)
    # if response.status_code == 200:
    #     forecast_data = json.loads(response.text)
    #     if isinstance(forecast_data, str):
    #         forecast_data = json.loads(forecast_data)
    #     return forecast_data
    # else:
    #     print(f"Error {response.status_code}: {response.text}")
    #     return None

# def convert_to_dataframe(forecast_data):
#     # Convert timestamps to datetime format
#     for data_point in forecast_data:
#         print(type(data_point))
#         data_point["ds"] = pd.to_datetime(int(data_point["ds"]), unit='ms')
        
#     # Convert the list to a DataFrame
#     df = pd.DataFrame(forecast_data)

#     return df

# App title
st.title("Live Stock Prices Dashboard")
#interval = "5T"  # adjust as needed
# Set up placeholders for dynamically updating content
kpi_placeholder = st.empty()
chart_placeholder1 = st.empty()
chart_placeholder2 = st.empty()
data_placeholder = st.empty()
forecast_placeholder = st.empty()

#print("forecast_data",forecast_data)
# forecast_df = None
# if forecast_data:
#     forecast_df = convert_to_dataframe(forecast_data)
while True:
    # Fetch data
    forecast_df = get_forecast(200,"5T")
    df = get_data()
    print("DDDDFFFFhead",df.head())
    print("DDDDFFFFtail",df.tail())
    print("DFFFFFLENGTH",df.shape[0])
    # Calculate KPIs
    avg_price = df["stock_price"].mean()
    last_price = df["stock_price"].iloc[0]
    oldest_price = df["stock_price"].iloc[-1]
    price_change = last_price - oldest_price

    # KPIs Display
    with kpi_placeholder.container():
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label="Average Stock Price 📊",
            value=f"${round(avg_price, 2)}"
        )

        kpi2.metric(
            label="Latest Stock Price 📈",
            value=f"${round(last_price, 2)}"
        )

        kpi3.metric(
            label="Price Change 💹",
            value=f"${round(price_change, 2)}",
            delta=round(price_change, 2)
        )

    # Plotting
    with chart_placeholder1.container():
        st.markdown("### Stock Price Over Time")
        fig = px.line(df, x='stock_date', y='stock_price', title='Stock Price Trend')
        if forecast_df is not None:
            print(forecast_df)
            print(forecast_df.info())
            fig.add_scatter(x=forecast_df["ds"], y=forecast_df["yhat"], mode='lines', name='Forecast', line=dict(color='red'))
        st.write(fig)

    with chart_placeholder2.container():
        st.markdown("### Price Distribution")
        fig2 = px.histogram(df, x='stock_price', title='Price Distribution')
        st.write(fig2)

    # Display data
    with data_placeholder.container():
        st.markdown("### Stock Data")
        st.dataframe(df)
    
    # Wait for a specific time interval before updating data
    time.sleep(10)  # Update every 10 seconds
