#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly
from yahoo_fin.stock_info import get_data
from ta.momentum import MACD
from ta.trend import RSIIndicator
import datetime

def main():
    # Function to load data
    @st.cache
    def load_data():
        stocks = get_data("RELIANCE.NS", start_date="01/01/2015", end_date="04/01/2023", index_as_date=True, interval="1d")
        stocks.drop('ticker', axis=1, inplace=True)
        stocks.reset_index(inplace=True)
        stocks.dropna(inplace=True)
        return stocks

    # Function to plot raw data
    def plot_raw_data(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['index'], y=data['open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['index'], y=data['close'], name="stock_close"))
        fig.update_layout(autosize=False, width=1000, height=600)
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    # Function for stock forecast
    def stock_forecast():
        data = load_data()
        st.subheader('Raw data')
        st.write(data.tail())
        plot_raw_data(data)

        # Forecasting
        days = st.slider('Days of predictions:', 1, 31)
        period = days * 1

        data_pred = data[['index', 'close']]
        data_pred = data_pred.rename(columns={"index": "ds", "close": "y"})

        m = Prophet()
        m.fit(data_pred)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Plot forecast
        fig = plot_plotly(m, forecast)
        st.write('Forecasting closing stock value for a period of:', days, 'days')
        st.plotly_chart(fig)

        # Plot component-wise forecast
        st.write("Component-wise forecast")
        fig = m.plot_components(forecast)
        st.write(fig)

    st.title('Stock Forecast App')

    if selected_page == 'page1':
        stock_forecast()

    elif selected_page == 'page2':
        # Function for technical indicators
        def technical_indicators():
            data = load_data()

            # Moving Average Convergence Divergence (MACD)
            macd = MACD(data['close']).macd()
            st.write('Stock Moving Average Convergence Divergence (MACD) = Close')
            st.area_chart(macd)

            # Resistance Strength Indicator (RSI)
            rsi = RSIIndicator(data['close']).rsi()
            st.write('Resistance Strength Indicator (RSI) = Close')
            st.line_chart(rsi)

        technical_indicators()

        # Forecasting
        years = st.slider('Years of predictions:', 1, 10)
        period = years * 365

        data_pred = load_data()[['index', 'close']]
        data_pred = data_pred.rename(columns={"index": "ds", "close": "y"})

        m = Prophet()
        m.fit(data_pred)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Plot forecast
        fig = plot_plotly(m, forecast)
        if st.checkbox('Show forecast data'):
            st.subheader('Forecast data')
            st.write(forecast)
        st.write('Forecasting closing stock value for a period of:', years, 'years')

    st.title('Stock Forecast App')

    selected_page = st.sidebar.selectbox("Select a page", ["page1", "page2"])

    if selected_page == 'page1':
        stock_forecast()

    elif selected_page == 'page2':
        technical_indicators()

        # Forecasting
        years = st.slider('Years of predictions:', 1, 10)
        period = years * 365

        data_pred = load_data()[['index', 'close']]
        data_pred = data_pred.rename(columns={"index": "ds", "close": "y"})

        m = Prophet()
        m.fit(data_pred)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Plot forecast
        fig = plot_plotly(m, forecast)
        if st.checkbox('Show forecast data'):
            st.subheader('Forecast data')
            st.write(forecast)
        st.write('Forecasting closing stock value for a period of:', years, 'years')

if __name__ == '__main__':
    main()

