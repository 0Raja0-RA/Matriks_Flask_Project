
from flask import Flask, render_template
from markupsafe import Markup
from pathlib import Path
import plotly.io as pio
from .viz_utils import load_data, create_timeseries_with_trend, create_moving_average, create_regression_plot, summary_stats
app = Flask(__name__, static_folder='static', template_folder='templates')
DATA_PATH = Path(__file__).parent / 'data' / 'zoo_visitors.csv'
@app.route('/')
def index():
    df = load_data(DATA_PATH); stats = summary_stats(df)
    preview = df.head().to_dict(orient='records')
    return render_template('index.html', stats=stats, preview=preview)
@app.route('/viz')
def viz():
    df = load_data(DATA_PATH)
    fig_trend, m, c = create_timeseries_with_trend(df, forecast_days=7)
    trend_div = pio.to_html(fig_trend, full_html=False, include_plotlyjs='cdn')
    fig_ma = create_moving_average(df, window=3)
    ma_div = pio.to_html(fig_ma, full_html=False, include_plotlyjs=False)
    fig_reg, m2, c2 = create_regression_plot(df)
    reg_div = pio.to_html(fig_reg, full_html=False, include_plotlyjs=False)
    return render_template('viz.html', trend_div=Markup(trend_div), ma_div=Markup(ma_div),
                           reg_div=Markup(reg_div), m=m, c=c, m2=m2, c2=c2)
@app.route('/conclusion')
def conclusion():
    df = load_data(DATA_PATH); stats = summary_stats(df)
    insights = []
    insights.append(f"Rata-rata pengunjung: {int(stats['average_visitors'])} orang/hari.")
    trend_dir = 'meningkat' if (df['visitors'].diff().mean() > 0) else 'menurun atau stagnan'
    insights.append(f"Arah tren: {trend_dir}.")
    return render_template('conclusion.html', stats=stats, insights=insights)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
