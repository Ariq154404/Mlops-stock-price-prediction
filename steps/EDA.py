import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.ingest import ingest_data
class TimeSeriesEDA:
    def __init__(self, df, date_col, value_col):
        self.df = df
        self.date_col = date_col
        self.value_col = value_col
        self.series = df.set_index(date_col)[value_col]
        print(self.series)

    def plot_series(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.series)
        plt.title('Time Series Plot')
        plt.xlabel(self.date_col)
        plt.ylabel(self.value_col)
        plt.xticks(self.series.index[::len(self.series)//10], rotation=45)
        plt.tight_layout()

        st.pyplot(plt)
        
    def decomposition(self):
        result = seasonal_decompose(self.series, model='additive', period=len(self.series)//10)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(10, 8))
    # Original Series
        ax1.plot(result.observed)
        ax1.set_title('Original Series')
        ax1.set_xticks([])
    
    # Trend
        ax2.plot(result.trend)
        ax2.set_title('Trend')
        ax2.set_xticks([])
    
    # Seasonality
        ax3.plot(result.seasonal)
        ax3.set_title('Seasonality')
        ax3.set_xticks([])
    
    # Residuals
        ax4.plot(result.resid)
        ax4.set_title('Residuals')
        ax4.set_xticks(result.observed.index[::len(self.series)//5])  # Adjust the spacing of x-ticks
        ax4.set_xticklabels(result.observed.index[::len(self.series)//5], rotation=45)  # Rotate x-tick labels for better visibility
    
        plt.tight_layout()
        st.pyplot(plt)

    def stationarity_test(self):
        result = adfuller(self.series)
        st.write('ADF Statistic:', result[0])
        st.write('p-value:', result[1])
        st.write('Critical Values:', result[4])

    def plot_acf_pacf(self):
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        plot_acf(self.series, ax=ax[0])
        plot_pacf(self.series, ax=ax[1])
        st.pyplot(plt)

    def run_all(self):
        self.plot_series()
        self.decomposition()
        self.stationarity_test()
        self.plot_acf_pacf()


def EDA(df : pd.DataFrame, date_col : str, value_col: str) -> None:
    st.title("Time Series EDA Dashboard")
        
    ts_eda = TimeSeriesEDA(df, date_col, value_col)
    ts_eda.run_all()

if __name__ == "__main__":
    df=ingest_data("localhost", "root", 3307, "my-secret-pw", "stocks")
    print(df.head())
    EDA(df,'stock_date','stock_price')