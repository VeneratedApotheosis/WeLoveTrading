# fetch_data.py
import yfinance as yf

#1. uses yfinance lib to fetch some basic btc data
df = yf.download("BTC-USD", start="2023-01-01", end="2026-01-01")

#2. process some stuff
#get returns (pct change from last candle)
df['Simple_Returns'] = df['Close'].pct_change()

df.to_csv("data/btc.csv")