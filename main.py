import sys; print(sys.executable)

import pandas as pd
import vectorbt as vbt
from strategies.trend_mac_strat import generate_signals

# 1. Load formatted data
df = pd.read_csv(
    'data/btc.csv', 
    skiprows=3, 
    names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], 
    index_col='Date', 
    parse_dates=True
)

# 2. Pass DataFrame to modular strategy
entries, exits = generate_signals(df)

# 3. Execute backtest
portfolio = vbt.Portfolio.from_signals(
    df['Close'], 
    entries, 
    exits, 
    init_cash=10000,
    fees=0.001 # 0.1% exchange fee
)

# 4. Output results
print(portfolio.stats())
# portfolio.plot().show() # Uncomment to render visual chart