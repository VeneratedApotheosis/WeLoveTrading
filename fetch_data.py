import yfinance as yf
import numpy as np
import pandas as pd
import os

# Create data folder if it doesn't exist
os.makedirs('data', exist_ok=True)

def refresh_data(symbol="BTC-USD"):
    # 1. Fetch
    df = yf.download(symbol, start="2023-01-01", end="2026-01-01")
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # 2. Calculate Simple Returns (Great for quick % checks)
    df['Simple_Return'] = df['Close'].pct_change()

    # 3. Calculate Log Returns (The "Pro" way for math/stats)
    # Formula: ln(Price_Today / Price_Yesterday)
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))

    # 4. Save
    df.to_csv("data/btc.csv")
    print(f"Data for {symbol} saved with Simple and Log returns.")

if __name__ == "__main__":
    refresh_data()