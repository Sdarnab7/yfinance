from flask import Flask, request, jsonify
import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochRSIIndicator
import pandas as pd

app = Flask(__name__)

@app.route('/api/indicators')
def indicators():
    ticker = request.args.get('ticker', 'TATAPOWER.NS')
    try:
        df = yf.download(ticker, period='3mo', interval='1d')
        if df.empty or 'Close' not in df.columns:
            return jsonify({'error': 'No data found for this ticker'}), 400

        close = df["Close"]  # ✅ 1D Series

        ema_12 = EMAIndicator(close, window=12).ema_indicator().iloc[-1]
        ema_26 = EMAIndicator(close, window=26).ema_indicator().iloc[-1]
        rsi = RSIIndicator(close, window=14).rsi().iloc[-1]
        stochrsi = StochRSIIndicator(close, window=14).stochrsi().iloc[-1]
        macd = MACD(close=close, window_fast=12, window_slow=26, window_sign=9).macd().iloc[-1]


        return jsonify({
            'ticker': ticker,
            'ema_12': float(ema_12),
            'ema_26': float(ema_26),
            'rsi': float(rsi),
            'stochrsi': float(stochrsi),
            'macd': float(macd)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
