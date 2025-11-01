
import pandas as pd, numpy as np
import plotly.graph_objects as go, plotly.express as px
from core.linalg import linear_regression
def load_data(path):
    df = pd.read_csv(path, parse_dates=['date']).sort_values('date').reset_index(drop=True)
    return df
def create_timeseries_with_trend(df, forecast_days=7):
    x = np.arange(len(df)); y = df['visitors'].to_numpy(float)
    m, c = linear_regression(x, y)
    future_x = np.arange(len(df) + forecast_days)
    y_pred = m*future_x + c
    timeline = pd.date_range(start=df['date'].min(), periods=len(future_x), freq='D')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=y, mode='lines+markers', name='Data Aktual'))
    fig.add_trace(go.Scatter(x=timeline, y=y_pred, mode='lines', name='Trend & Prediksi'))
    fig.update_layout(title=f"Trend & Prediksi — y = {m:.2f}x + {c:.2f}", xaxis_title="Tanggal",
                      yaxis_title="Pengunjung", template="plotly_white")
    return fig, m, c
def create_moving_average(df, window=3):
    df_ma = df.copy(); df_ma['MA'] = df_ma['visitors'].rolling(window=window, min_periods=1).mean()
    fig = px.line(df_ma, x='date', y=['visitors','MA'], title=f"Moving Average (window={window})")
    fig.update_layout(template="plotly_white"); return fig
def create_regression_plot(df):
    x = np.arange(len(df)); y = df['visitors'].to_numpy(float)
    m, c = linear_regression(x, y); y_line = m*x + c
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=y, mode='markers', name='Data'))
    fig.add_trace(go.Scatter(x=df['date'], y=y_line, mode='lines', name='Garis Regresi'))
    fig.update_layout(title=f"Regresi Linier — y = {m:.2f}x + {c:.2f}", xaxis_title="Tanggal",
                      yaxis_title="Pengunjung", template="plotly_white")
    return fig, m, c
def summary_stats(df):
    return {
        'rows': int(len(df)),
        'columns': int(df.shape[1]),
        'start_date': str(df['date'].min().date()),
        'end_date': str(df['date'].max().date()),
        'average_visitors': float(df['visitors'].mean()),
        'median_visitors': float(df['visitors'].median()),
        'max_visitors': int(df['visitors'].max()),
        'max_visitors_date': str(df.loc[df['visitors'].idxmax(),'date'].date()),
        'min_visitors': int(df['visitors'].min()),
        'min_visitors_date': str(df.loc[df['visitors'].idxmin(),'date'].date()),
    }
