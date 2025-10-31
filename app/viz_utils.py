import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)
    return df

def create_timeseries_with_trend(df, forecast_days=7):
    # simple linear trend forecast
    x = np.arange(len(df))
    y = df['visitors'].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)
    # future
    future_x = np.arange(len(df) + forecast_days)
    future_dates = pd.date_range(df['date'].min(), periods=len(future_x), freq='D')
    future_y = trend(future_x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=y, mode='lines+markers', name='Actual Visitors', marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=future_dates, y=future_y, mode='lines', name='Trend & Prediction', line=dict(dash='dash')))
    fig.update_layout(title='Zoo Visitors — Trend & Prediction',
                      xaxis_title='Date', yaxis_title='Visitors', template='plotly_white')
    return fig, coef

def create_moving_average(df, window=3):
    df_ma = df.copy()
    df_ma['ma'] = df_ma['visitors'].rolling(window=window, min_periods=1).mean()
    fig = px.line(df_ma, x='date', y=['visitors','ma'], labels={'value':'Visitors','date':'Date'}, title=f'Moving Average (window={window})')
    fig.update_layout(template='plotly_white')
    return fig

def summary_stats(df):
    stats = {}
    stats['rows'] = len(df)
    stats['columns'] = df.shape[1]
    stats['start_date'] = str(df['date'].min().date())
    stats['end_date'] = str(df['date'].max().date())
    stats['average_visitors'] = float(df['visitors'].mean())
    stats['median_visitors'] = float(df['visitors'].median())
    stats['max_visitors'] = int(df['visitors'].max())
    stats['max_visitors_date'] = str(df.loc[df['visitors'].idxmax(),'date'].date())
    stats['min_visitors'] = int(df['visitors'].min())
    stats['min_visitors_date'] = str(df.loc[df['visitors'].idxmin(),'date'].date())
    return stats