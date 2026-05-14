import pandas as pd
import vectorbt as vbt
import itertools

# Import your modular logic
from strategies.adaptive_zscore_sma import generate_signals
from configs.portfolio_profiles import get_strategy_exit_profile

# 1. Load Data
df = pd.read_csv('data/btc.csv', index_col='Date', parse_dates=True)

# 2. Define the Parameter Grid
# Be careful: adding too many numbers will make this run for hours!
fast_smas = [22, 25, 30, 35]
slow_smas = [50, 60, 70, 80]
z_lengths = [25,30,35]
z_buys = [-1.5, -2.0]

# Generate all possible combinations
combinations = list(itertools.product(fast_smas, slow_smas, z_lengths, z_buys))
print(f"Testing {len(combinations)} different parameter combinations...")

# 3. Run the Grid Search
results = []

for fast, slow, z_len, z_buy in combinations:
    # Skip illogical combinations (Fast SMA must be faster than Slow SMA)
    if fast >= slow:
        continue
        
    # Generate signals with current parameters
    entries, exits = generate_signals(
        df, 
        fast_len=fast, 
        slow_len=slow, 
        z_len=z_len, 
        z_buy=z_buy
    )
    
    # Load profile and run backtest
    profile = get_strategy_exit_profile(df, entries, exits)
    portfolio = vbt.Portfolio.from_signals(**profile)
    
    # Extract key metrics
    try:
        total_return = portfolio.stats()['Total Return [%]']
        win_rate = portfolio.stats()['Win Rate [%]']
        profit_factor = portfolio.stats()['Profit Factor']
        max_drawdown = portfolio.stats()['Max Drawdown [%]']
        
        results.append({
            'Fast SMA': fast,
            'Slow SMA': slow,
            'Z Length': z_len,
            'Z Buy Threshold': z_buy,
            'Return (%)': total_return,
            'Win Rate (%)': win_rate,
            'Profit Factor': profit_factor,
            'Max Drawdown (%)': max_drawdown
        })
    except Exception as e:
        # Sometimes a terrible parameter combination takes 0 trades, causing an error
        pass

results_df = pd.DataFrame(results)

n_top = 7

top_profit = results_df.sort_values(by='Profit Factor', ascending=False).head(n_top)
top_return = results_df.sort_values(by='Return (%)', ascending=False).head(n_top)
top_drawdown = results_df.sort_values(by='Max Drawdown (%)', ascending=True).head(n_top)

print("\n=== TOP Return ===")
print(top_return.to_string(index=False))

print("\n=== TOP Profit ===")
print(top_profit.to_string(index=False))

print("\n=== TOP Drawdown ===")
print(top_drawdown.to_string(index=False))