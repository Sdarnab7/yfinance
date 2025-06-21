from flask import Flask, request, jsonify
import yfinance as yf
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochRSIIndicator

app = Flask(__name__)

@app.route('/api/indicators')
def indicators():
    ticker = request.args.get('ticker', 'TATAPOWER.NS')
    df = yf.download(ticker, period='3mo', interval='1d')
    if df.empty:
        return jsonify({"error": "Invalid ticker or no data"}), 400

    ema_12 = EMAIndicator(df["Close"], window=12).ema_indicator()
    ema_26 = EMAIndicator(df["Close"], window=26).ema_indicator()
    rsi = RSIIndicator(df["Close"], window=14).rsi()
    stochrsi = StochRSIIndicator(df["Close"], window=14).stochrsi()
    macd = MACD(df["Close"]).macd()

    result = {
        "ticker": ticker,
        "ema_12": float(ema_12.iloc[-1]),
        "ema_26": float(ema_26.iloc[-1]),
        "rsi": float(rsi.iloc[-1]),
        "stochrsi": float(stochrsi.iloc[-1]),
        "macd": float(macd.iloc[-1])
    }
    return jsonify(result)
