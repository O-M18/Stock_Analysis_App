import streamlit as st
from pages.utils.model import get_data,get_forecast,rolling_mean,model_fit,stationary_check,scaling,inverse_scale,diff_order,evaluate_model
from pages.utils.plotly_fig import Plotly_table,Moving_avg_forecast
import pandas as pd
import datetime
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downward_trend",
    layout="wide"
)
st.title("Stock Prediction")

today=datetime.date.today()
col1,col2,col3 =st.columns(3)

it_sector_tickers = {"Apple": "AAPL","Google": "GOOGL","Amazon": "AMZN","Meta Platforms": "META",
    "NVIDIA": "NVDA","Cisco Systems": "CSCO","Intel": "INTC","Adobe": "ADBE","Salesforce": "CRM",
    "Oracle": "ORCL","IBM": "IBM","ServiceNow": "NOW","Broadcom": "AVGO","Qualcomm": "QCOM"}
with col1:
    company = st.selectbox("Company", list(it_sector_tickers.keys()))
    ticker = it_sector_tickers[company]
with col2:
    start_date=st.date_input("choose start date",datetime.date(today.year-1,today.month,today.day))
with col3:
    end_date = st.date_input("choose end date", datetime.date(today.year, today.month, today.day))
rmse=0

st.subheader(" Predicting Price For Next 30 Days Of "+ticker)
close_price=get_data(ticker,start_date,end_date)
rolling_price=rolling_mean(close_price)
diffencing_order=diff_order(close_price)
scaled_data,scaler=scaling(rolling_price)
rmse=evaluate_model(scaled_data,diffencing_order)

st.write("**Model RMSE Score:**",rmse)
forecast=get_forecast(scaled_data,diffencing_order)
forecast["Close"]=inverse_scale(scaler,forecast["Close"])
st.write("##### Forecast data (Next 30 Days)")
fig_tail=Plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=250)
st.plotly_chart(fig_tail,use_container_width=True)
rolling_price.columns=['Close']
forecast=pd.concat([rolling_price,forecast])
st.plotly_chart(Moving_avg_forecast(forecastgit),use_container_width=True)
