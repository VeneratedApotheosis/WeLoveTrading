import pandas_ta as ta

def generate_signals(df, z_len=30, base_z=-2.0, atr_len=14, baseline_len=100):
    
    # 1. Standard Z-Score
    zscore = ta.zscore(df['Close'], length=z_len)
    
    # 2. Normalized ATR (Volatility as a percentage of price)
    # This standardizes volatility across $3k BTC and $70k BTC
    natr = ta.natr(df['High'], df['Low'], df['Close'], length=atr_len)
    
    # 3. Historical Volatility Baseline
    # What is the "average" volatility over the last 100 days?
    natr_baseline = ta.sma(natr, length=baseline_len)
    
    # 4. THE DYNAMIC THRESHOLD MATH
    volatility_ratio = natr / natr_baseline
    
    # Multiply our base Z-score (-2.0) by the ratio. 
    # If volatility is high (ratio > 1), threshold becomes stricter (e.g., -3.0).
    dynamic_z_threshold = base_z * volatility_ratio
    
    # We cap it using .clip() so it never becomes EASIER than -2.0.
    # It can only get stricter.
    dynamic_z_threshold = dynamic_z_threshold.clip(upper=base_z)

    # 5. THE "DEAD MARKET" GATE
    # If current volatility is less than 70% of the historical average, do not trade!
    is_market_awake = natr > (natr_baseline * 0.7)

    # --- GENERATE SIGNALS ---
    
    # Buy: Market is awake AND Z-score drops below our constantly changing threshold
    buy_condition = (zscore < dynamic_z_threshold) & is_market_awake
    
    # Trigger only on the exact day it crosses
    entries = buy_condition & (~buy_condition.shift(1).fillna(False))
    
    # Sell: Return to the mean
    exits = (zscore > 0) & (zscore.shift(1) <= 0)

    return entries, exits