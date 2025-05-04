import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader as web
from pages.utils.plotly_fig import interactive_chart,normalize,daily_return,beta_calculated
st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upward_trend",
    layout="wide"
)
st.title("Capital Assest Pricing Model")
col1, col2, col3=st.columns(3)
today=datetime.date.today()
it_sector_tickers = {"Apple": "AAPL","Alphabet": "GOOGL","Amazon": "AMZN","Meta Platforms": "META",
                     "NVIDIA": "NVDA","Cisco Systems": "CSCO","Intel": "INTC","Adobe": "ADBE","Salesforce": "CRM",
                     "Oracle": "ORCL","IBM": "IBM","ServiceNow": "NOW","Broadcom": "AVGO","Qualcomm": "QCOM"}
col1,col2=st.columns([1,1])
with col1:
    stock_list=st.multiselect("Choose 4 Stock",list(it_sector_tickers.keys()),['Apple','Alphabet','Amazon','Meta Platforms'])
with col2:
    year=st.number_input("Number of years",1,10)
    
start=datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
SP500=web.DataReader(['sp500'],'fred',start,today)

stock_df=pd.DataFrame()
for stock in stock_list:
    data=yf.download(it_sector_tickers[stock],period=f"{year}y")
    stock_df[stock]=data['Close']

stock_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns=['Date','sp500']
stock_df=pd.merge(stock_df,SP500,on='Date',how='inner')

col1,col2=st.columns([1,1])
with col1:
    st.markdown("#### TOP 10 DATA")
    st.dataframe(stock_df.head(10),use_container_width=True)
    # fig_df=Plotly_table(stock_df.head(10))
    # st.plotly_chart(fig_df,use_container_width=True)
with col2:
    st.markdown("#### BOTTOM 10")
    st.dataframe(stock_df.tail(10),use_container_width=True)
    # fig_df=Plotly_table(stock_df.tail(10))
    # st.plotly_chart(fig_df,use_container_width=True)
    
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Stock Prices")
    st.plotly_chart(interactive_chart(stock_df))
with col2:
    st.markdown('### Normalize Value')
    st.plotly_chart(interactive_chart(normalize(stock_df)))
    
daily_return=daily_return(stock_df)

aplha={}
beta={}

for i in daily_return.columns:
    if i !='Date' and i !='sp500':
        b,a=beta_calculated(daily_return,i)
        
        beta[i]=b
        aplha[i]=a

beta_df=pd.DataFrame(columns=['Stock','Beta value'])
beta_df['Stock']=beta.keys()
beta_df['Beta value']=[ round(i,2) for i in beta.values()]

with col1:
    st.markdown("### Beta value")
    st.dataframe(beta_df,use_container_width=True)
   
rf=0
rm=daily_return['sp500'].mean()*252
return_df=pd.DataFrame()
return_value=[]
for stock, value in beta.items():
    return_value.append(round(rf+(value*(rm-rf)),2))
return_df['Stock']=stock_list
return_df['Return value']=return_value

with col2:
    st.markdown("### Return using CAPM")
    st.dataframe(return_df,use_container_width=True)
        
    