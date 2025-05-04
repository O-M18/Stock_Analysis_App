import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
# import ta
from pages.utils.plotly_fig import Plotly_table,Candlestick,Line_chart,MACD,RSI,Moving_average
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide"
)
st.title("Stock Analysis")
col1, col2, col3=st.columns(3)
today=datetime.date.today()
it_sector_tickers = {"Apple": "AAPL","Alphabet": "GOOGL","Amazon": "AMZN","Meta Platforms": "META",
                     "NVIDIA": "NVDA","Cisco Systems": "CSCO","Intel": "INTC","Adobe": "ADBE","Salesforce": "CRM",
                     "Oracle": "ORCL","IBM": "IBM","ServiceNow": "NOW","Broadcom": "AVGO","Qualcomm": "QCOM"}

with col1:
    company=st.selectbox("Company",list(it_sector_tickers.keys()))
    Ticker=it_sector_tickers[company]
with col2:
    start_date=st.date_input("choose start date",datetime.date(today.year-1,today.month,today.day))
with col3:
    end_date = st.date_input("choose end date", datetime.date(today.year, today.month, today.day))
    
st.subheader(Ticker)
stock=yf.Ticker(Ticker)
st.write(stock.info["longBusinessSummary"])
st.write(stock.info["sector"])
st.write(stock.info["fullTimeEmployees"])
st.write(stock.info["website"])

col1, col2=st.columns(2)
with col1:
    df=pd.DataFrame(index=['Market Cap','Beta','EPS','PE Ratio'])
    df['']=[stock.info['marketCap'],stock.info['beta'],stock.info['trailingEps'],stock.info['trailingPE']]
    fig_df=Plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)
with col2:
    df=pd.DataFrame(index=['Quick Ratio','Revenue per share','Profit Margins','Debt to Equity','Return on Equity'])
    df['']=[stock.info['quickRatio'],stock.info['revenuePerShare'],stock.info['profitMargins'],
            stock.info['debtToEquity'],stock.info['returnOnEquity']]
    fig_df=Plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)
    
data=yf.download(Ticker,start=start_date,end=end_date)
col1, col2,col3 =st.columns(3)
daily_changes=data['Close'].iloc[-1]-data['Close'].iloc[-2]
percentage_change = (daily_changes / data['Close'].iloc[-2]) * 100
# col1.metric("Daily changes",str(round(data['Close'].iloc[-1],2)),str(round(daily_changes,2)))
col1.metric("Daily Changes", round(daily_changes, 2), f"{round(percentage_change, 2)}%")
last_10day=data.tail(10).sort_index(ascending=False).round(3)
last_10day.columns = [' '.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in last_10day.columns]
fig_df=Plotly_table(last_10day)
st.write("#### Historical data(Last 10days)")
st.plotly_chart(fig_df,use_container_width=True)

col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12=st.columns([1,1,1,1,1,1,1,1,1,1,1,1])
num_period=""
with col1:
    if st.button('5D'):
        num_period='5d'
with col2:
    if st.button("1M"):
        num_period='1mo'
with col3:
    if st.button("6M"):
        num_period='6mo'
with col4:
    if st.button("YTD"):
        num_period='ytd'
with col5:
    if st.button("1Y"):
        num_period='1y'
with col6:
    if st.button("5Y"):
        num_period='5y'    
with col7:
    if st.button("Max"):
        num_period='max'
        
col1,col2,col3=st.columns([1,1,4])
with col1:
    chart_type=st.selectbox('',("Candle","Line"))
with col2:
    if chart_type=="Candle":
        indicators=st.selectbox('',('RSI','MACD'))
    else:
        indicators=st.selectbox('',('RSI','Moving Average','MACD'))
        
ticker_=yf.Ticker(Ticker)
new_diff=ticker_.history(period="max")
data_1=ticker_.history(period='max')
if num_period=="":
    if chart_type=="Candle" and indicators=="RSI":
        st.plotly_chart(Candlestick(data_1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data_1,'1y'),use_container_width=True)
        
    if chart_type=="Candle" and indicators=="MACD":
        st.plotly_chart(Candlestick(data_1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data_1,'1y'),use_container_width=True)
        
    if chart_type=="Line" and indicators=="RSI":
        st.plotly_chart(Line_chart(data_1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data_1,'1y'),use_container_width=True)
        
    if chart_type=="Line" and indicators=="Moving Average":
        st.plotly_chart(Moving_average(data_1,'1y'),use_container_width=True)
        
    if chart_type=="Line" and indicators=="MACD":
        st.plotly_chart(Line_chart(data_1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data_1,'1y'),use_container_width=True)

else:

    if chart_type == "Candle" and indicators=="RSI":
        st.plotly_chart(Candlestick(new_diff, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_diff,num_period), use_container_width=True)

    if chart_type == "Candle" and indicators=="MACD":
        st.plotly_chart(Candlestick(new_diff,num_period), use_container_width=True)
        st.plotly_chart(MACD(new_diff,num_period), use_container_width=True)

    if chart_type == "Line" and indicators=="RSI":
        st.plotly_chart(Line_chart(new_diff,num_period), use_container_width=True)
        st.plotly_chart(RSI(new_diff,num_period), use_container_width=True)

    if chart_type == "Line" and indicators=="Moving Average":
        st.plotly_chart(Moving_average(new_diff,num_period), use_container_width=True)

    if chart_type == "Line" and indicators=="MACD":
        st.plotly_chart(Line_chart(new_diff,num_period), use_container_width=True)
        st.plotly_chart(MACD(new_diff,num_period), use_container_width=True)
    
    