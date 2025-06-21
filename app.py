from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochRSIIndicator
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/indicators')
def indicators():
    ticker = request.args.get('ticker', 'TATAPOWER.NS')

    try:
        df = yf.download(ticker, period='3mo', interval='1d')

        if df.empty or 'Close' not in df.columns:
            return jsonify({'error': 'No data found for this ticker'}), 400

        # Explicitly ensure 1D Series
        close = df["Close"].squeeze()
        if isinstance(close, pd.DataFrame):
            return jsonify({'error': 'Close is a DataFrame, not Series'}), 500

        if close.ndim != 1:
            return jsonify({'error': f'Close column is {close.ndim}D'}), 500

        # Indicators (all strictly passed a 1D Series)
        ema_12 = EMAIndicator(close=close, window=12).ema_indicator().iloc[-1]
        ema_26 = EMAIndicator(close=close, window=26).ema_indicator().iloc[-1]
        rsi = RSIIndicator(close=close, window=14).rsi().iloc[-1]
        stochrsi = StochRSIIndicator(close=close, window=14).stochrsi().iloc[-1]
        macd = MACD(close=close, window_fast=12, window_slow=26, window_sign=9).macd().iloc[-1]

        return jsonify({
            'ticker': ticker,
            'ema_12': round(float(ema_12), 2),
            'ema_26': round(float(ema_26), 2),
            'rsi': round(float(rsi), 2),
            'stochrsi': round(float(stochrsi), 2),
            'macd': round(float(macd), 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
