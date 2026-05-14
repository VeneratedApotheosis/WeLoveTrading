# main.py
import sys; print(sys.executable)
import pandas as pd
import vectorbt as vbt

# Import logic and configs
from strategies.test import generate_signals
from configs.portfolio_profiles import get_tsl_profile, get_strategy_exit_profile

# 1. Load data
df = pd.read_csv('data/btc.csv', index_col='Date', parse_dates=True)

# 2. Generate signals
entries, exits = generate_signals(df)

# 3. SELECT YOUR PROFILE HERE
# To test the Trailing Stop, use this line:
portfolio_kwargs = get_strategy_exit_profile(df, entries, exits)

# To test the RSI-exit strategy, comment out the line above and use this one:
# portfolio_kwargs = get_strategy_exit_profile(df, entries, exits)

# 4. Execute backtest using dictionary unpacking (**)
portfolio = vbt.Portfolio.from_signals(**portfolio_kwargs)

# 5. Output results
print(portfolio.stats())
portfolio.plot().show()