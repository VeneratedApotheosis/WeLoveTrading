import pandas_ta as ta

def generate_signals(df, window=30, z_buy=-2.0, z_sell=0.0):
    # 1. Calculate the Z-Score
    # Formula: (Close - SMA) / Standard Deviation
    zscore = ta.zscore(df['Close'], length=window)
    
    # --- DEFINE CONDITIONS ---
    
    # Buy exactly when the Z-Score drops below our extreme threshold (e.g., -2.0)
    # The shift(1) logic ensures we only trigger a signal on the exact day it crosses
    entries = (zscore < z_buy) & (zscore.shift(1) >= z_buy)
    
    # Sell exactly when the Z-score crosses back up over our sell threshold (e.g., 0.0)
    exits = (zscore > z_sell) & (zscore.shift(1) <= z_sell)

    return entries, exits