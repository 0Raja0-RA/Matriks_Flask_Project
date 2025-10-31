from flask import Flask, render_template, Markup
from pathlib import Path
import json
from .viz_utils import load_data, create_timeseries_with_trend, create_moving_average, summary_stats
import plotly.io as pio

app = Flask(__name__, static_folder='static', template_folder='templates')

DATA_PATH = Path(__file__).parent / 'data' / 'zoo_visitors.csv'

@app.route('/')
def index():
    df = load_data(DATA_PATH)
    stats = summary_stats(df)
    # small preview
    preview = df.head().to_dict(orient='records')
    return render_template('index.html', stats=stats, preview=preview)

@app.route('/viz')
def viz():
    df = load_data(DATA_PATH)
    fig_trend, coef = create_timeseries_with_trend(df, forecast_days=7)
    fig_ma = create_moving_average(df, window=3)
    # convert to html divs
    trend_div = pio.to_html(fig_trend, full_html=False, include_plotlyjs='cdn')
    ma_div = pio.to_html(fig_ma, full_html=False, include_plotlyjs=False)
    # basic predictive summary using coef
    slope = float(coef[0])
    intercept = float(coef[1])
    pred_next_week = sum([slope*(len(df)+i) + intercept for i in range(7)])/7.0
    pred_summary = {
        'trend_slope': round(slope,2),
        'predicted_avg_next_week': round(pred_next_week,2),
        'trend_direction': 'increasing' if slope>0 else 'decreasing'
    }
    return render_template('viz.html', trend_div=Markup(trend_div), ma_div=Markup(ma_div), pred_summary=pred_summary)

@app.route('/conclusion')
def conclusion():
    df = load_data(DATA_PATH)
    stats = summary_stats(df)
    # simple insights
    insights = []
    insights.append(f"Rata-rata pengunjung selama periode: {int(stats['average_visitors'])} orang/hari.")
    insights.append(f"Hari dengan pengunjung tertinggi: {stats['max_visitors_date']} ({stats['max_visitors']} orang).")
    insights.append(f"Tren linier menunjukkan arah: {'meningkat' if (df['visitors'].diff().mean()>0) else 'menurun'}.")
    insights.append("Prediksi sederhana (linear) menunjukkan kemungkinan kenaikan pengunjung jika kondisi sama.")
    return render_template('conclusion.html', stats=stats, insights=insights)

if __name__ == '__main__':
    app.run(debug=True)