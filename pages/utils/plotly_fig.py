import pandas_ta as pta
import plotly.graph_objects as go
import dateutil
import numpy as np
import plotly.express as exp
import datetime
def Plotly_table(dataframe):
    header="red"
    rowevencolor="#A6AEBF"
    rowoddcolor="#C5D3E8"
    fig=go.Figure(data=[go.Table(
    header=dict(
        values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
        line_color="#789DBC",fill_color="#789DBC",
        align="center",font=dict(color="white",size=15),height=35
        ),
    cells=dict(
        values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns],
        line_color=["#789DBC"],fill_color=[[rowoddcolor,rowevencolor]],
        align="left",font=dict(color=["black"],size=15)
        )
    )])
    fig.update_layout(height=400,margin=dict(l=0,t=0,b=0,r=0))
    return fig


def Filter_date(data_frame,num_period):
    if num_period=='1mo':
        date=data_frame.index[-1]+ dateutil.relativedelta.relativedelta(months=-1)
    elif num_period=='5d':
        date = data_frame.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period=='6mo':
        date = data_frame.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period=='1y':
        date = data_frame.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period=='5y':
        date = data_frame.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period=='ytd':
        date = datetime.datetime(data_frame.index[-1].year,1,1).strftime('%Y-%m-%d')
    else:
        date=data_frame.index[0]
    return data_frame.reset_index()[data_frame.reset_index()['Date']>date]
def Line_chart(data_frame,num_period=False):
    if num_period:
        data_frame=Filter_date(data_frame,num_period)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data_frame['Date'],y=data_frame['Open'],mode='lines',
                             name='Open',line=dict(width=2,color='#F9D923')))
    fig.add_trace(go.Scatter(x=data_frame['Date'],y=data_frame['Close'],mode='lines',
                             name='Close',line=dict(width=2,color='#F9D923')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['High'], mode='lines',
                             name='High', line=dict(width=2, color='#EB5353')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['Low'], mode='lines',
                             name = 'Low', line = dict(width=2, color='#187498')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),paper_bgcolor='#D2E0FB',plot_bgcolor='white',
                      legend=dict(xanchor='right',yanchor='top',font_color='black'))
    return  fig


def Candlestick(data_frame,num_period):
    data_frame=Filter_date(data_frame,num_period)
    fig=go.Figure()
    fig.add_trace(go.Candlestick(x=data_frame['Date'],low=data_frame['Low'],
                             open=data_frame['Open'],close=data_frame['Close'],high=data_frame['High']))
    
    fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),paper_bgcolor='#D2E0FB',plot_bgcolor='white',
                      legend=dict(xanchor='right',yanchor='top'))
    return fig

def RSI(data_frame,num_period):
    data_frame['RSI']=pta.rsi(data_frame['Close'])
    data_frame=Filter_date(data_frame, num_period)
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(x=data_frame['Date'],y=data_frame.RSI,
                             name='RSI',line=dict(width=2,color='#FFA500'))
    )
    fig.add_trace(
        go.Scatter(x=data_frame['Date'],y=[70]*len(data_frame),
                             name='Overbought',line=dict(width=2,color='#32CD32',dash='dash'))
    )
    fig.add_trace(
        go.Scatter(x=data_frame['Date'], y=[30] * len(data_frame),
                   name='Underbought',fill='tonexty', line=dict(width=2, color='#79da84', dash='dash'))
    )
    fig.update_layout(
        yaxis_range=[0,1000],height=200,plot_bgcolor='white',paper_bgcolor='#D2E0FB',
        margin=dict(t=0,r=0,l=0,b=0),
        legend=dict(orientation='h',yanchor='top',y=1.02,xanchor='right',x=1,font_color='black')
        
    )
    return fig

def Moving_average(data_frame,num_period):
    data_frame['SMA']=pta.sma(data_frame['Close'],50)
    data_frame=Filter_date(data_frame, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['Open'], mode='lines',
                             name='Open', line=dict(width=2, color='#F9D923')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['Close'], mode='lines',
                             name='Close', line=dict(width=2, color='#F9D923')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['High'], mode='lines',
                             name='High', line=dict(width=2, color='#EB5353')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['Low'], mode='lines',
                             name='Low', line=dict(width=2, color='#187498')))
    fig.add_trace(go.Scatter(x=data_frame['Date'], y=data_frame['SMA'], mode='lines',
                             name='SMA', line=dict(width=2, color='#97900F')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), paper_bgcolor='#D2E0FB', plot_bgcolor='white',
                      legend=dict(xanchor='right', yanchor='top',font_color='black'))
    return fig

def MACD(data_frame,num_period):
    macd=pta.macd(data_frame['Close']).iloc[:,0]
    macd_signal=pta.macd(data_frame['Close']).iloc[:,1]
    macd_his=pta.macd(data_frame['Close']).iloc[:,2]
    data_frame['MACD']=macd
    data_frame['macd_signal']=macd_signal
    data_frame['macd_his']=macd_his
    data_frame=Filter_date(data_frame, num_period)
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data_frame.index,y=data_frame['MACD'],
            name='MACD',line=dict(width=2,color='orange')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data_frame.index, y=data_frame['macd_signal'],
            name='Overbrought', line=dict(width=2, color='red',dash='dash')
        )
    )
    c=[ 'red' if cl <0 else 'green' for cl in macd_his]
    fig.update_layout(
         height=200, plot_bgcolor='white', paper_bgcolor='#D2E0FB',
        margin=dict(t=0, r=0, l=0, b=0),
        legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='right', x=1, font_color='white')
    )
    return fig

def Moving_avg_forecast(forecast):
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=forecast.index[:-30],y=forecast["Close"].iloc[:-30],
            mode="lines",name="Close price",line=dict(width=2,color="#2FA4FF")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast.index[-30:], y=forecast["Close"].iloc[-30:],
            mode="lines", name=" Future close price", line=dict(width=2, color="#00FFDD")
        )
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0,t=25,r=25,b=0),plot_bgcolor="white",
                      paper_bgcolor="white",legend=dict(xanchor="right",yanchor="top",font_color='black'))
    
    return fig

def interactive_chart(df):
    fig=exp.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width=400,margin=dict(l=20,r=20,t=50,b=40),legend=dict(orientation='h',yanchor='bottom',
                                                                             y=1.02,xanchor='right',x=1))
    return fig

def normalize(df):
    df_2=df.copy()
    for i in df_2.columns[1:]:
        df_2[i]=df_2[i]/df_2[i][0]
    return df_2

def daily_return(df):
    df_re=df.copy()
    for i in df_re.columns[1:]:
        for j in range(1,len(df_re)):
            df_re[i][j]=((df_re[i][j]-df_re[i][j-1])/df_re[i][j-1])*100
        df_re[i][0]=0
    return df_re

def beta_calculated(daily_return,stock):
    rm=daily_return["sp500"].mean()*252
    
    b,a=np.polyfit(daily_return['sp500'],daily_return[stock],1)
    return b,a
    
        


