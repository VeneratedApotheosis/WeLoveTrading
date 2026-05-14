import pandas_ta as ta

def generate_signals(df, fast_len=20, slow_len=50, z_len=30, z_buy=-1.5, sma_len=200):
    
    # 1. CALCULATE ALL INDICATORS (Using the custom variables)
    sma_200 = ta.sma(df['Close'], length=sma_len)
    fast_sma = ta.sma(df['Close'], length=fast_len)
    slow_sma = ta.sma(df['Close'], length=slow_len)
    zscore = ta.zscore(df['Close'], length=z_len)
    
    # 2. REGIMES
    regime_trending = df['Close'] > sma_200
    regime_sideways = df['Close'] <= sma_200

    # 3. STATES
    state_sma_bullish = fast_sma > slow_sma
    state_zscore_oversold = zscore < z_buy

    # 4. MASTER BUY STATE
    trend_buy_condition = regime_trending & state_sma_bullish
    sideways_buy_condition = regime_sideways & state_zscore_oversold
    master_buy_state = trend_buy_condition | sideways_buy_condition

    # 5. ENTRY
    entries = master_buy_state & (~master_buy_state.shift(1).fillna(False))

    # 6. EXITS
    trend_exit = (fast_sma < slow_sma) & (fast_sma.shift(1) >= slow_sma.shift(1))
    sideways_exit = (zscore > 0) & (zscore.shift(1) <= 0)
    
    exits = trend_exit | sideways_exit

    return entries, exits