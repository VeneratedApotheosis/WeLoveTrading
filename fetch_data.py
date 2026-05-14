# fetch_data.py
import yfinance as yf

# uses yfinance lib to fetch some basic btc data
df = yf.download("BTC-USD", start="2020-01-01", end="2026-01-01")
df.to_csv("data/btc.csv")