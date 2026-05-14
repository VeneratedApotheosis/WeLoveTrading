import pandas_ta as ta

def generate_signals(df):
    
    # 2. Calculate Indicators on RETURNS instead of Close
    # Note: 200 is a very long window for daily returns; 
    # it will stay very close to 0.00 (the average daily gain).
    sma_200_ret = ta.sma(df['Simple_Returns'], length=200)
    
    # MACD on returns measures the 'momentum of the momentum'
    macd = ta.macd(df['Simple_Returns'], fast=12, slow=26, signal=9)
    macd_line = macd['MACD_12_26_9']
    signal_line = macd['MACDs_12_26_9']

    # 3. Define Conditions
    # Is the average return over the last 200 days positive?
    trend_bull = sma_200_ret > 0 
    
    # MACD Crossovers on the return series
    macd_cross_up = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
    macd_cross_down = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))

    # 4. Generate Signal Arrays
    entries = trend_bull & macd_cross_up
    exits = macd_cross_down

    return entries, exits