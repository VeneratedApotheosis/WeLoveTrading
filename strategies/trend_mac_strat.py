import pandas_ta as ta

def generate_signals(df):
    # 1. Calculate Indicators
    sma_200 = ta.sma(df['Close'], length=200)
    macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    macd_line = macd['MACD_12_26_9']
    signal_line = macd['MACDs_12_26_9']

    # 2. Define Conditions
    trend_bull = df['Close'] > sma_200
    macd_cross_up = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
    macd_cross_down = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))

    # 3. Generate Signal Arrays
    entries = trend_bull & macd_cross_up
    exits = macd_cross_down

    return entries, exits