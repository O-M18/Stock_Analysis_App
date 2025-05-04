import yfinance as yf
import pandas as pd
from sklearn.metrics import mean_squared_error,r2_score
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from datetime import datetime,timedelta
from sklearn.preprocessing import StandardScaler
import numpy as np


def get_data(ticker,start_date,end_date):
    stock_data=yf.download(ticker,start=start_date,end=end_date)
    return stock_data[['Close']]

def stationary_check(close_price):
    test=adfuller(close_price)
    p_value=round(test[1],3)
    return p_value

def rolling_mean(close_price):
    rollin_price=close_price.rolling(window=7).mean().dropna()
    return rollin_price
def diff_order(close_price):
    p_value=stationary_check(close_price)
    d=0
    while True:
        if p_value>0.05:
            d+=1
            close_price=close_price.diff().dropna()
            p_value=stationary_check(close_price)
        else:
            break
    return d
def model_fit(data,diff_order):
    model=ARIMA(data,order=(30,diff_order,30))
    model_fit=model.fit()
    
    forecast_step=30
    forecast=model_fit.get_forecast(steps=forecast_step)
    prediction=forecast.predicted_mean
    return prediction

def evaluate_model(original_price,diff_order):
    train,test=original_price[:-30],original_price[-30:]
    prediction=model_fit(train,diff_order)
    rmse=np.sqrt(mean_squared_error(test,prediction))
    return round(rmse,2)
def scaling(close_prcie):
    scaler=StandardScaler()
    scaled_data=scaler.fit_transform(np.array(close_prcie).reshape(-1,1))
    return scaled_data,scaler
def get_forecast(original_price,diff_order):
    prediction=model_fit(original_price,diff_order)
    start=datetime.now().strftime("%Y-%m-%d")
    end=(datetime.now()+timedelta(days=29)).strftime("%Y-%m-%d")
    forecast_index=pd.date_range(start=start,end=end,freq="D")
    forecast_df=pd.DataFrame(prediction,index=forecast_index,columns=['Close'])
    return forecast_df
def inverse_scale(scaler,scaled_data):
    close_price=scaler.inverse_transform(np.array(scaled_data).reshape(-1,1))
    return close_price
    